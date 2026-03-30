# Migration to convert string degree_type values to ForeignKey references

from django.db import migrations


def convert_degree_type_strings_to_fk(apps, schema_editor):
    """Convert existing string degree_type values to ProgramIntrest ForeignKey references"""
    Program = apps.get_model('academics', 'Program')
    ProgramIntrest = apps.get_model('academics', 'ProgramIntrest')
    
    # Mapping of old string values to new ProgramIntrest entries
    degree_mapping = {
        'bachelor': ("Bachelor's Degree", 1),
        'master': ("Master's Degree", 2),
        'certificate': ('Certificate', 3),
        'diploma': ('Diploma', 4),
    }
    
    # Create ProgramIntrest objects first
    for string_val, (name, id_val) in degree_mapping.items():
        pi, created = ProgramIntrest.objects.get_or_create(
            id=id_val,
            defaults={'name': name}
        )
    
    # Now we need to update the Program records
    # But we can't do this in the RunPython because the field is still a CharField
    # This migration just creates the ProgramIntrest records
    # The actual data migration will happen when we convert the field type


def reverse_convert(apps, schema_editor):
    """Reverse is not supported for this migration"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0005_programintrest'),
    ]

    operations = [
        migrations.RunPython(convert_degree_type_strings_to_fk, reverse_convert),
    ]
