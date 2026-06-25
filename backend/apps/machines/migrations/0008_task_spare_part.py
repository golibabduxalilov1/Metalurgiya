from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0007_repairtask_assignee_due_date'),
        ('warehouse', '0002_unit_of_measure'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskSparePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_used', models.DecimalField(decimal_places=3, max_digits=15, verbose_name='Ishlatilgan miqdor')),
                ('deducted', models.BooleanField(default=False, verbose_name='Ombordan ayirildi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('spare_part', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='task_usages',
                    to='warehouse.sparepart',
                    verbose_name='Ehtiyot qism',
                )),
                ('task', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='spare_parts_used',
                    to='machines.repairtask',
                    verbose_name='Vazifa',
                )),
            ],
            options={
                'verbose_name': 'Vazifadagi ehtiyot qism',
                'verbose_name_plural': 'Vazifadagi ehtiyot qismlar',
                'db_table': 'task_spare_parts',
            },
        ),
    ]
