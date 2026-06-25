from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0010_maintenancehistory_repair_started_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksparepart',
            name='cost',
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=15,
                null=True, verbose_name='Xarajat (dollar)'
            ),
        ),
        migrations.AddField(
            model_name='maintenancehistory',
            name='total_cost',
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=15,
                verbose_name='Jami xarajat'
            ),
        ),
    ]
