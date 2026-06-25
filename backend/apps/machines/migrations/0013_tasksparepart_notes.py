from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0012_repairtask_assignee_to_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksparepart',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Izoh'),
        ),
    ]
