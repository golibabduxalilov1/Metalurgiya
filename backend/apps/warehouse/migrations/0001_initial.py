from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('machines', '0004_maintenance_schedule'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SparePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Цена')),
                ('supplier', models.CharField(blank=True, max_length=300, verbose_name='Поставщик')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='created_spare_parts',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('machines', models.ManyToManyField(
                    blank=True,
                    related_name='spare_parts',
                    to='machines.machine',
                    verbose_name='Станки',
                )),
            ],
            options={
                'verbose_name': 'Запчасть',
                'verbose_name_plural': 'Запчасти',
                'db_table': 'spare_parts',
                'ordering': ['name'],
            },
        ),
    ]
