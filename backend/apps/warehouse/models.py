from django.db import models
from django.conf import settings


class SparePart(models.Model):
    """Запчасти и расходные материалы"""
    name = models.CharField('Наименование', max_length=300)
    price = models.DecimalField(
        'Цена', max_digits=15, decimal_places=2, null=True, blank=True
    )
    supplier = models.CharField('Поставщик', max_length=300, blank=True)
    machines = models.ManyToManyField(
        'machines.Machine',
        related_name='spare_parts',
        verbose_name='Станки',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='created_spare_parts',
        null=True, blank=True
    )

    class Meta:
        db_table = 'spare_parts'
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        ordering = ['name']

    def __str__(self):
        return self.name
