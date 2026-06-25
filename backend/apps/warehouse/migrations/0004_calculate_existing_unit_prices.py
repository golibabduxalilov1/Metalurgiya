from django.db import migrations


def calculate_unit_prices(apps, schema_editor):
    SparePart = apps.get_model('warehouse', 'SparePart')
    updated = 0
    for sp in SparePart.objects.filter(unit_price__isnull=True):
        if sp.price is not None and sp.quantity and sp.quantity != 0:
            sp.unit_price = sp.price / sp.quantity
            sp.save(update_fields=['unit_price'])
            updated += 1
    print(f'  unit_price calculated for {updated} spare parts.')


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_sparepart_unit_price'),
    ]

    operations = [
        migrations.RunPython(calculate_unit_prices, migrations.RunPython.noop),
    ]
