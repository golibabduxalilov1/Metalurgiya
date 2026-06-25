from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_unit_of_measure'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparepart',
            name='unit_price',
            field=models.DecimalField(
                blank=True, decimal_places=4, max_digits=15,
                null=True, verbose_name='Birlik narxi'
            ),
        ),
    ]
