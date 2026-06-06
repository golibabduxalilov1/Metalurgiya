"""
Machines App Models - Core business models for machine registry
"""
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator


class MachineType(models.Model):
    """Справочник типов станков"""
    name = models.CharField('Тип станка', max_length=200, unique=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'machine_types'
        verbose_name = 'Тип станка'
        verbose_name_plural = 'Типы станков'
        ordering = ['name']

    def __str__(self):
        return self.name


class MachineStatus(models.Model):
    """Справочник статусов станков"""
    class Color(models.TextChoices):
        GREEN = 'green', 'Зелёный'
        YELLOW = 'yellow', 'Жёлтый'
        RED = 'red', 'Красный'
        GRAY = 'gray', 'Серый'
        BLUE = 'blue', 'Синий'

    name = models.CharField('Статус', max_length=100, unique=True)
    color = models.CharField('Цвет', max_length=10, choices=Color.choices, default=Color.GRAY)
    is_active = models.BooleanField('Активен', default=True)
    requires_comment = models.BooleanField('Требует комментарий', default=False)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'machine_statuses'
        verbose_name = 'Статус станка'
        verbose_name_plural = 'Статусы станков'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Machine(models.Model):
    """Основной реестр станков"""
    # Основные поля
    name = models.CharField('Наименование', max_length=300)
    inventory_number = models.CharField('Инвентарный номер', max_length=100, unique=True)
    model = models.CharField('Модель', max_length=200, blank=True)
    manufacturer = models.CharField('Производитель', max_length=200, blank=True)
    year_manufactured = models.PositiveIntegerField('Год выпуска', null=True, blank=True)
    commissioned_date = models.DateField('Дата ввода в эксплуатацию', null=True, blank=True)

    # Связанные справочники
    machine_type = models.ForeignKey(
        MachineType, on_delete=models.PROTECT,
        related_name='machines', verbose_name='Тип станка',
        null=True, blank=True
    )
    current_status = models.ForeignKey(
        MachineStatus, on_delete=models.PROTECT,
        related_name='machines', verbose_name='Текущий статус',
        null=True, blank=True
    )
    workshop = models.ForeignKey(
        'workshops.Workshop', on_delete=models.SET_NULL,
        related_name='machines', verbose_name='Цех',
        null=True, blank=True
    )
    section = models.ForeignKey(
        'workshops.Section', on_delete=models.SET_NULL,
        related_name='machines', verbose_name='Участок',
        null=True, blank=True
    )
    workplace = models.CharField('Рабочее место', max_length=100, blank=True)

    # Оператор/бригада
    assigned_operator = models.ForeignKey(
        'employees.Employee', on_delete=models.SET_NULL,
        related_name='assigned_machines', verbose_name='Оператор',
        null=True, blank=True
    )
    assigned_brigade = models.CharField('Бригада', max_length=200, blank=True)

    # Дополнительно
    description = models.TextField('Описание / Комментарий', blank=True)

    # Soft delete
    deleted_at = models.DateTimeField('Удалён', null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='deleted_machines', null=True, blank=True
    )

    # Метаданные
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='created_machines', null=True, blank=True
    )

    class Meta:
        db_table = 'machines'
        verbose_name = 'Станок'
        verbose_name_plural = 'Станки'
        ordering = ['inventory_number']
        indexes = [
            models.Index(fields=['inventory_number']),
            models.Index(fields=['deleted_at']),
            models.Index(fields=['current_status']),
            models.Index(fields=['workshop']),
        ]

    def __str__(self):
        return f"{self.inventory_number} — {self.name}"

    @property
    def is_deleted(self):
        return self.deleted_at is not None


class MachineStatusHistory(models.Model):
    """История изменения статусов станка"""
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE,
        related_name='status_history', verbose_name='Станок'
    )
    previous_status = models.ForeignKey(
        MachineStatus, on_delete=models.SET_NULL,
        related_name='history_from', verbose_name='Предыдущий статус',
        null=True, blank=True
    )
    new_status = models.ForeignKey(
        MachineStatus, on_delete=models.PROTECT,
        related_name='history_to', verbose_name='Новый статус'
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='status_changes', verbose_name='Изменил',
        null=True, blank=True
    )
    comment = models.TextField('Причина / Комментарий', blank=True)
    changed_at = models.DateTimeField('Дата изменения', auto_now_add=True)

    class Meta:
        db_table = 'machine_status_history'
        verbose_name = 'История статусов'
        verbose_name_plural = 'История статусов'
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.machine} → {self.new_status} ({self.changed_at:%d.%m.%Y %H:%M})"


class MachineAttachment(models.Model):
    """Файлы и документы, прикреплённые к станку"""
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx']

    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE,
        related_name='attachments', verbose_name='Станок'
    )
    file = models.FileField(
        'Файл', upload_to='machines/attachments/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)]
    )
    original_filename = models.CharField('Оригинальное имя файла', max_length=255)
    file_size = models.PositiveBigIntegerField('Размер файла (байт)', default=0)
    content_type = models.CharField('Тип файла', max_length=100)
    description = models.CharField('Описание', max_length=500, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='uploaded_files', null=True, blank=True
    )
    uploaded_at = models.DateTimeField('Загружен', auto_now_add=True)

    class Meta:
        db_table = 'machine_attachments'
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.machine}: {self.original_filename}"


class MachineAssignment(models.Model):
    """История закрепления операторов за станком"""
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE,
        related_name='assignments', verbose_name='Станок'
    )
    operator = models.ForeignKey(
        'employees.Employee', on_delete=models.CASCADE,
        related_name='assignments', verbose_name='Оператор'
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='machine_assignments', null=True, blank=True
    )
    assigned_at = models.DateTimeField('Закреплён', auto_now_add=True)
    unassigned_at = models.DateTimeField('Откреплён', null=True, blank=True)
    is_current = models.BooleanField('Текущее', default=True)
    notes = models.TextField('Примечания', blank=True)

    class Meta:
        db_table = 'machine_assignments'
        verbose_name = 'Закрепление оператора'
        verbose_name_plural = 'Закрепления операторов'
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.machine} ← {self.operator}"
