from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0005_maintenance_repair_started'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Vazifa')),
                ('is_done', models.BooleanField(default=False, verbose_name='Bajarildi')),
                ('done_at', models.DateTimeField(blank=True, null=True, verbose_name='Bajarilgan vaqt')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('schedule', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tasks',
                    to='machines.maintenanceschedule',
                    verbose_name='График ТО',
                )),
            ],
            options={
                'verbose_name': 'Remont vazifasi',
                'verbose_name_plural': 'Remont vazifalari',
                'db_table': 'repair_tasks',
                'ordering': ['created_at'],
            },
        ),
    ]
