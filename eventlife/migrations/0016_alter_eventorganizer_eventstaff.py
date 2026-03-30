# Generated migration to add null=True to eventstaff field

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventlife', '0015_alter_eventorganizer_phone_no_delete_eventcalender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventorganizer',
            name='eventstaff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventstaff', to='faculty.staff'),
        ),
    ]
