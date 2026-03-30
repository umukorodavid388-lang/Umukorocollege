from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from addmission.models import StudentRegistration
from .models import AlumniSuccess, Alumni


@receiver(post_save, sender=StudentRegistration)
def create_alumni_success_on_completion(sender, instance, created, update_fields, **kwargs):
    """
    Automatically create AlumniSuccess record when a student completes their program
    and passes (status='completed' AND is_passed=True)
    """
    # Check if student has completed and passed
    if instance.status == 'completed' and instance.is_passed:
        # Check if success story already exists for this student
        if not AlumniSuccess.objects.filter(
            name=instance.student_name
        ).exists():
            
            # Create Alumni record if it doesn't exist
            alumni, _ = Alumni.objects.get_or_create(
                email=instance.student_email,
                defaults={
                    'first_name': instance.student_name.split()[0] if ' ' in instance.student_name else instance.student_name,
                    'last_name': instance.student_name.split()[-1] if ' ' in instance.student_name else '',
                    'graduation_year': instance.completion_date.year if instance.completion_date else timezone.now().year,
                    'program': instance.program.title,
                    'profile_image': instance.pics if instance.pics else None,
                }
            )
            
            # Create success story
            AlumniSuccess.objects.create(
                alumni=alumni,
                name=instance.student_name,
                graduation_year=instance.completion_date.year if instance.completion_date else timezone.now().year,
                position=f"Graduate - {instance.program.title}",
                organization="Alumnus",
                description=f"Successfully completed {instance.program.title} program with grade {instance.grades or 'A'}.",
                image=instance.pics,
                is_featured=False,
                order=0,
            )
