from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0009_maintenance_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancehistory',
            name='repair_started_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Remont boshlangan vaqt'),
        ),
    ]
