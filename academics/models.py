from django.db import models

# Create your models here.

class ProgramIntrest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    


class Program(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='media/academics/', help_text="Program icon/image")
    duration = models.CharField(max_length=100, help_text="e.g., 4 Years")
    degree_type = models.ForeignKey(ProgramIntrest, on_delete=models.CASCADE, help_text="Degree type", related_name='degree_programs')
    is_featured = models.BooleanField(default=False, help_text="Display as main featured program")
    order = models.PositiveIntegerField(default=0, help_text="Order of display in programs grid")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def students_count(self):
        """Count total registered students in this program"""
        return self.registrations.filter(status='enrolled').count()
    
    @property
    def success_rate(self):
        """Calculate success rate based on completed students"""
        total_registrations = self.registrations.exclude(status='dropped').count()
        if total_registrations == 0:
            return 0
        
        successful_students = self.registrations.filter(status='completed', is_passed=True).count()
        rate = (successful_students / total_registrations) * 100
        return round(rate, 2)

