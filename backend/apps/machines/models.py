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

    # Стоимость и амортизация
    initial_cost = models.DecimalField(
        'Начальная стоимость', max_digits=15, decimal_places=2, null=True, blank=True
    )
    useful_life_years = models.PositiveIntegerField(
        'Срок полезного использования (лет)', null=True, blank=True
    )
    residual_value = models.DecimalField(
        'Ликвидационная стоимость', max_digits=15, decimal_places=2,
        null=True, blank=True, default=None
    )

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

    @property
    def amortization_info(self):
        if not self.initial_cost or not self.useful_life_years:
            return None
        from decimal import Decimal
        import datetime
        from django.utils import timezone

        initial = self.initial_cost
        residual = self.residual_value if self.residual_value is not None else Decimal('0')
        years = self.useful_life_years
        annual = (initial - residual) / years

        if self.commissioned_date:
            today = timezone.now().date()
            days_used = (today - self.commissioned_date).days
            years_used = min(days_used / 365.25, years)
        else:
            years_used = 0

        accumulated = annual * Decimal(str(round(years_used, 6)))
        book_value = max(initial - accumulated, residual)

        return {
            'annual_depreciation': round(annual, 2),
            'years_used': round(years_used, 2),
            'accumulated_depreciation': round(accumulated, 2),
            'book_value': round(book_value, 2),
        }


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


class MaintenanceSchedule(models.Model):
    """График технического обслуживания (ТО) станка"""
    machine = models.OneToOneField(
        Machine, on_delete=models.CASCADE,
        related_name='maintenance_schedule', verbose_name='Станок'
    )
    interval_months = models.PositiveIntegerField('Интервал ТО (месяцев)')
    last_maintenance_date = models.DateField('Дата последнего ТО', null=True, blank=True)
    next_maintenance_date = models.DateField('Дата следующего ТО')
    notes = models.TextField('Примечания', blank=True)
    repair_started_at = models.DateTimeField('Начало ремонта', null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='created_maintenance_schedules', null=True, blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='updated_maintenance_schedules', null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'maintenance_schedules'
        verbose_name = 'График ТО'
        verbose_name_plural = 'Графики ТО'
        ordering = ['next_maintenance_date']

    def __str__(self):
        return f"ТО: {self.machine} → {self.next_maintenance_date}"

    @property
    def tasks_total(self):
        return self.tasks.count()

    @property
    def tasks_done(self):
        return self.tasks.filter(is_done=True).count()

    @property
    def days_until(self):
        from django.utils import timezone
        delta = self.next_maintenance_date - timezone.now().date()
        return delta.days

    @property
    def in_repair(self):
        return self.repair_started_at is not None

    @property
    def alert_level(self):
        if self.in_repair:
            return 'in_repair'
        days = self.days_until
        if days < 0:
            return 'overdue'
        if days <= 7:
            return 'near'
        return 'ok'


class RepairTask(models.Model):
    """Vazifalar ro'yxati — remont davomidagi topshiriqlar"""
    schedule = models.ForeignKey(
        MaintenanceSchedule, on_delete=models.CASCADE,
        related_name='tasks', verbose_name='График ТО'
    )
    title = models.CharField('Vazifa', max_length=500, blank=True, default='')
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='repair_tasks', verbose_name='Mas\'ul foydalanuvchi'
    )
    due_date = models.DateField('Bajarilish muddati', null=True, blank=True)
    is_done = models.BooleanField('Bajarildi', default=False)
    done_at = models.DateTimeField('Bajarilgan vaqt', null=True, blank=True)
    has_bonus = models.BooleanField('Yonlanma', default=False)
    bonus_amount = models.DecimalField(
        'Yonlanma summasi', max_digits=15, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'repair_tasks'
        verbose_name = 'Remont vazifasi'
        verbose_name_plural = 'Remont vazifalari'
        ordering = ['created_at']

    def __str__(self):
        return self.title


class MaintenanceHistory(models.Model):
    """TO tarixi — har bir remont yakunlanganida yaratiladi"""
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE,
        related_name='maintenance_history', verbose_name='Stanok'
    )
    repair_started_at = models.DateTimeField('Remont boshlangan vaqt', null=True, blank=True)
    completed_at = models.DateTimeField('Yakunlangan vaqt', auto_now_add=True)
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Bajargan'
    )
    interval_months = models.PositiveIntegerField('Interval (oy)', default=0)
    notes = models.TextField('Izoh', blank=True)
    tasks_snapshot = models.JSONField('Vazifalar snapshot', default=list)
    total_cost = models.DecimalField('Jami xarajat', max_digits=15, decimal_places=2, default=0)

    class Meta:
        db_table = 'maintenance_history'
        verbose_name = 'TO tarixi'
        verbose_name_plural = 'TO tarixi'
        ordering = ['-completed_at']

    def __str__(self):
        return f"TO: {self.machine} — {self.completed_at.date()}"


class TaskSparePart(models.Model):
    """Vazifada ishlatilgan ehtiyot qism"""
    task = models.ForeignKey(
        RepairTask, on_delete=models.CASCADE,
        related_name='spare_parts_used', verbose_name='Vazifa'
    )
    spare_part = models.ForeignKey(
        'warehouse.SparePart', on_delete=models.CASCADE,
        related_name='task_usages', verbose_name='Ehtiyot qism'
    )
    quantity_used = models.DecimalField(
        'Ishlatilgan miqdor', max_digits=15, decimal_places=3
    )
    notes = models.TextField('Izoh', blank=True)
    cost = models.DecimalField(
        'Xarajat (dollar)', max_digits=15, decimal_places=2, null=True, blank=True
    )
    deducted = models.BooleanField('Ombordan ayirildi', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_spare_parts'
        verbose_name = 'Vazifadagi ehtiyot qism'
        verbose_name_plural = 'Vazifadagi ehtiyot qismlar'

    def __str__(self):
        return f"{self.task} — {self.spare_part} x{self.quantity_used}"


class ExchangeRate(models.Model):
    """So'm/USD kursi — bitta yozuv sifatida saqlanadi"""
    usd_to_som = models.DecimalField(
        '1 USD = ? so\'m', max_digits=12, decimal_places=2, default=12700
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exchange_rate'
        verbose_name = 'Valyuta kursi'
        verbose_name_plural = 'Valyuta kurslari'

    def __str__(self):
        return f"1 USD = {self.usd_to_som} so'm"

    @classmethod
    def get_current(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
