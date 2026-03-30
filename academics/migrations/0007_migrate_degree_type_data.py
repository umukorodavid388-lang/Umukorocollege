# Generated migration to handle degree_type field conversion and data migration

import django.db.models.deletion
from django.db import migrations, models


def migrate_data_and_field(apps, schema_editor):
    """
    This function runs SQL directly to:
    1. Add a temporary bigint column
    2. Map the old string values to new IDs
    3. Drop the old column
    4. Rename the new column
    """
    # Execute raw SQL to handle the conversion
    schema_editor.execute("""
        ALTER TABLE academics_program ADD COLUMN degree_type_new bigint;
        
        UPDATE academics_program 
        SET degree_type_new = CASE 
            WHEN degree_type = 'bachelor' THEN 1
            WHEN degree_type = 'master' THEN 2
            WHEN degree_type = 'certificate' THEN 3
            WHEN degree_type = 'diploma' THEN 4
            ELSE NULL
        END;
        
        ALTER TABLE academics_program DROP COLUMN degree_type;
        ALTER TABLE academics_program RENAME COLUMN degree_type_new TO degree_type;
        
        ALTER TABLE academics_program 
        ADD CONSTRAINT academics_program_degree_type_fk 
        FOREIGN KEY (degree_type) 
        REFERENCES academics_programintrest(id) 
        ON DELETE CASCADE;
    """)


def reverse_migrate(apps, schema_editor):
    """Reverse is not supported"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0006_convert_degree_type_to_fk'),
    ]

    operations = [
        migrations.RunPython(migrate_data_and_field, reverse_migrate),
    ]
