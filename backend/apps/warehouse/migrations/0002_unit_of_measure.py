from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('short_name', models.CharField(blank=True, max_length=20, verbose_name='Сокращение')),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
                'db_table': 'units_of_measure',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='sparepart',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True, verbose_name='Количество'),
        ),
        migrations.AddField(
            model_name='sparepart',
            name='unit',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='spare_parts',
                to='warehouse.unitofmeasure',
                verbose_name='Единица измерения',
            ),
        ),
    ]
