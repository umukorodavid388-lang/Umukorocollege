from django.db import models
from django.utils import timezone
from datetime import datetime


class Alumni(models.Model):
    """Model to store alumni information"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    graduation_year = models.IntegerField()
    program = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='media/alumni/', blank=True, null=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-graduation_year']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.graduation_year})"


class AlumniSuccess(models.Model):
    """Model to store success stories of alumni"""
    alumni = models.OneToOneField(Alumni, related_name='success_story', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150)
    graduation_year = models.IntegerField()
    position = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/alumni_success/')
    story_link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
    def get_class_year(self):
        """Return class year in format 'Class of YYYY'"""
        return f"Class of {self.graduation_year}"


class Campus(models.Model):
    """Model to track campuses around the world"""
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Campuses"
        ordering = ['country', 'city']
    
    def __str__(self):
        return f"{self.name} - {self.country}"


class AlumniNetwork(models.Model):
    """Track overall alumni network statistics with dynamic calculations"""
    founding_year = models.IntegerField(default=1960, help_text="Year the institution was founded")
    description = models.TextField(default="")
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Alumni Network"
        verbose_name_plural = "Alumni Network"
    
    def __str__(self):
        return "Alumni Network Statistics"
    
    @property
    def total_alumni_worldwide(self):
        """Dynamically count total alumni (students with completed status)"""
        from addmission.models import StudentRegistration
        return StudentRegistration.objects.filter(
            status='completed',
            is_passed=True
        ).count()
    
    @property
    def total_countries(self):
        """Dynamically count number of countries where campuses are located"""
        return Campus.objects.filter(is_active=True).values('country').distinct().count() or 118
    
    @property
    def years_of_excellence(self):
        """Dynamically calculate years since founding"""
        current_year = datetime.now().year
        return current_year - self.founding_year
    
    @property
    def total_campuses(self):
        """Get total number of active campuses"""
        return Campus.objects.filter(is_active=True).count()
