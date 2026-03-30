from django.db import models
from academics.models import *
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.



class StudentRegistration(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended'),
    ]

    pics = models.ImageField(upload_to='media/addmission/')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='registrations')
    student_name = models.CharField(max_length=200)
    student_email = models.EmailField(unique=True)
    student_phone = models.CharField(max_length=20, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    is_passed = models.BooleanField(default=False, help_text="Check if student completed successfully")
    grades = models.CharField(max_length=5, blank=True, help_text="e.g., A, B, C, D, F")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ('program', 'student_email')
    
    def __str__(self):
        return f"{self.student_name} - {self.program.title} ({self.status})"


class ApplicationStep(models.Model):
    """Model for application steps (How to Apply)"""
    step_number = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['step_number']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class AdmissionRequirement(models.Model):
    """Model for admission requirements"""
    requirement = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    note = models.TextField(blank=True)
    is_mandatory = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.requirement


class TuitionProgram(models.Model):

    """Model for tuition and fees by program"""
    program_name = models.ForeignKey(ProgramIntrest, related_name='program_interest', on_delete=models.CASCADE)
    tuition_per_year = models.DecimalField(max_digits=10, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.program_name)
    
    @property
    def total_per_year(self):
        return self.tuition_per_year + self.fees


class TutionNote(models.Model):
    finicial = models.CharField(max_length=200)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.finicial


class AdmissionDeadline(models.Model):
    """Model for important admission deadlines"""
    deadline_name = models.CharField(max_length=100)
    deadline_date = models.DateField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'deadline_date']
    
    def __str__(self):
        return f"{self.deadline_name} - {self.deadline_date}"


class InformationRequest(models.Model):
    """Model for admission information requests from contact form"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('rejected', 'Rejected'),
    ]

    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    program = models.ForeignKey(ProgramIntrest, related_name='addmission_information_requests', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    is_contacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.program}" if self.program else f"{self.name} - No Program"


class CampusVisitRequest(models.Model):
    """Model for campus visit booking"""
    VISIT_TYPE_CHOICES = [
        ('in_person', 'In-Person Tour'),
        ('virtual', 'Virtual Tour'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES, default='in_person')
    number_of_visitors = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    special_requests = models.TextField(blank=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.preferred_date} ({self.visit_type})"
    


class CampusVisst(models.Model):
    """ Model for campus visiting """
    picture = models.ImageField(upload_to='media/addmission/')
    content = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True)


    def __str__(self):
        return self.title


class CampusVisitContent(models.Model):
    icon = models.CharField(max_length=100, help_text="CSS class for icon, e.g., fa fa-check")
    text = models.CharField(max_length=200)
    campus = models.ForeignKey(CampusVisst, related_name='campus', on_delete=models.CASCADE)

    def __str__(self):
        return self.text