from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def clear_assignees(apps, schema_editor):
    # Clear existing Employee references before changing FK target
    schema_editor.execute("UPDATE repair_tasks SET assignee_id = NULL")


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0011_cost_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # First clear old Employee IDs (they won't map to User IDs)
        migrations.RunPython(clear_assignees, migrations.RunPython.noop),
        # Now safely alter the FK to point to User
        migrations.AlterField(
            model_name='repairtask',
            name='assignee',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='repair_tasks',
                to=settings.AUTH_USER_MODEL,
                verbose_name="Mas'ul foydalanuvchi",
            ),
        ),
    ]
