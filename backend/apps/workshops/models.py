"""
Workshops App - Справочник цехов и участков
"""
from django.db import models


class Workshop(models.Model):
    """Цех"""
    name = models.CharField('Наименование цеха', max_length=200, unique=True)
    code = models.CharField('Код', max_length=20, blank=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workshops'
        verbose_name = 'Цех'
        verbose_name_plural = 'Цеха'
        ordering = ['name']

    def __str__(self):
        return self.name


class Section(models.Model):
    """Участок (привязан к цеху)"""
    workshop = models.ForeignKey(
        Workshop, on_delete=models.CASCADE,
        related_name='sections', verbose_name='Цех'
    )
    name = models.CharField('Наименование участка', max_length=200)
    code = models.CharField('Код', max_length=20, blank=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sections'
        verbose_name = 'Участок'
        verbose_name_plural = 'Участки'
        ordering = ['workshop', 'name']
        unique_together = [['workshop', 'name']]

    def __str__(self):
        return f"{self.workshop.name} / {self.name}"
