from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0008_task_spare_part'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True, verbose_name='Yakunlangan vaqt')),
                ('interval_months', models.PositiveIntegerField(default=0, verbose_name='Interval (oy)')),
                ('notes', models.TextField(blank=True, verbose_name='Izoh')),
                ('tasks_snapshot', models.JSONField(default=list, verbose_name='Vazifalar snapshot')),
                ('completed_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Bajargan',
                )),
                ('machine', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='maintenance_history',
                    to='machines.machine',
                    verbose_name='Stanok',
                )),
            ],
            options={
                'verbose_name': 'TO tarixi',
                'verbose_name_plural': 'TO tarixi',
                'db_table': 'maintenance_history',
                'ordering': ['-completed_at'],
            },
        ),
    ]
