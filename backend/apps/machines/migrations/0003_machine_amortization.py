from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='initial_cost',
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=15,
                null=True, verbose_name='Начальная стоимость'
            ),
        ),
        migrations.AddField(
            model_name='machine',
            name='useful_life_years',
            field=models.PositiveIntegerField(
                blank=True, null=True,
                verbose_name='Срок полезного использования (лет)'
            ),
        ),
        migrations.AddField(
            model_name='machine',
            name='residual_value',
            field=models.DecimalField(
                blank=True, decimal_places=2, default=None, max_digits=15,
                null=True, verbose_name='Ликвидационная стоимость'
            ),
        ),
    ]
