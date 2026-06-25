from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('machines', '0006_repair_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairtask',
            name='assignee',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='repair_tasks',
                to='employees.employee',
                verbose_name="Mas'ul xodim",
            ),
        ),
        migrations.AddField(
            model_name='repairtask',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='Bajarilish muddati'),
        ),
    ]
