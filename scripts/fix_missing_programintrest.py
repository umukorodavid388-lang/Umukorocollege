import os
import sys
import pathlib
import django

# Ensure project root (parent of this `college` package) is on PYTHONPATH
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college.settings')
django.setup()

from addmission.models import InformationRequest, TuitionProgram, StudentRegistration
from academics.models import ProgramIntrest, Program

ids = set(InformationRequest.objects.values_list('program_id', flat=True)) | set(TuitionProgram.objects.values_list('program_name_id', flat=True))
ids.discard(None)
existing = set(ProgramIntrest.objects.values_list('id', flat=True))
missing = ids - existing

if not missing:
    print('No missing ProgramIntrest ids found')
else:
    print('Missing ids:', missing)
    for mid in missing:
        obj, created = ProgramIntrest.objects.get_or_create(id=mid, defaults={'name': f'Placeholder id {mid}'})
        print('Created' if created else 'Exists', obj.id, obj.name)

print('Done')

# Now check for missing Program (academics.Program) ids referenced by addmission models
program_ids = set(InformationRequest.objects.values_list('program_id', flat=True)) | set(StudentRegistration.objects.values_list('program_id', flat=True))
program_ids.discard(None)
existing_programs = set(Program.objects.values_list('id', flat=True))
missing_programs = program_ids - existing_programs

if not missing_programs:
    print('No missing Program ids found')
else:
    print('Missing Program ids:', missing_programs)
    for pid in missing_programs:
        # Get or create a default ProgramIntrest
        degree_type_obj, _ = ProgramIntrest.objects.get_or_create(
            name='Certificate',
            defaults={'id': 3}  # Use id 3 for certificate
        )
        defaults = {
            'title': f'Placeholder Program {pid}',
            'description': 'Placeholder created during migration',
            'icon': 'media/academics/placeholder.png',
            'duration': 'N/A',
            'degree_type': degree_type_obj,
        }
        obj, created = Program.objects.get_or_create(id=pid, defaults=defaults)
        print('Created' if created else 'Exists', obj.id, obj.title)

print('All done')
