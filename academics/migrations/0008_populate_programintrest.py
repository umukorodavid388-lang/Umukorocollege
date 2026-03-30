# Generated migration to populate ProgramIntrest with degree types

from django.db import migrations


def populate_program_interest(apps, schema_editor):
    ProgramIntrest = apps.get_model('academics', 'ProgramIntrest')
    
    degree_types = [
        {'id': 1, 'name': "Bachelor's Degree"},
        {'id': 2, 'name': "Master's Degree"},
        {'id': 3, 'name': 'Certificate'},
        {'id': 4, 'name': 'Diploma'},
    ]
    
    for degree in degree_types:
        ProgramIntrest.objects.get_or_create(
            id=degree['id'],
            defaults={'name': degree['name']}
        )


def reverse_populate(apps, schema_editor):
    ProgramIntrest = apps.get_model('academics', 'ProgramIntrest')
    ProgramIntrest.objects.filter(id__in=[1, 2, 3, 4]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0007_migrate_degree_type_data'),
    ]

    operations = [
        migrations.RunPython(populate_program_interest, reverse_populate),
    ]
