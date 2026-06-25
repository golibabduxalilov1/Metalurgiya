from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0004_maintenance_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenanceschedule',
            name='repair_started_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Начало ремонта'),
        ),
    ]
