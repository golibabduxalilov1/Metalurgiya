from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0003_machine_amortization'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval_months', models.PositiveIntegerField(verbose_name='Интервал ТО (месяцев)')),
                ('last_maintenance_date', models.DateField(blank=True, null=True, verbose_name='Дата последнего ТО')),
                ('next_maintenance_date', models.DateField(verbose_name='Дата следующего ТО')),
                ('notes', models.TextField(blank=True, verbose_name='Примечания')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('machine', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='maintenance_schedule',
                    to='machines.machine',
                    verbose_name='Станок',
                )),
                ('created_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='created_maintenance_schedules',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('updated_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='updated_maintenance_schedules',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'График ТО',
                'verbose_name_plural': 'Графики ТО',
                'db_table': 'maintenance_schedules',
                'ordering': ['next_maintenance_date'],
            },
        ),
    ]
