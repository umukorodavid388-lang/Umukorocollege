from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Hero (models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    picture = models.ImageField(upload_to='media/website/')

    def __str__(self):
        return self.title   



class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=100, help_text="bi bi-text")
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name='features')

    def __str__(self):
        return self.name


class UpcomingEvent(models.Model):
    event_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    rsvp_url = models.URLField(blank=True, null=True)
    hero = models.OneToOneField(Hero, on_delete=models.CASCADE, related_name='upcoming_event', null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def day(self):
        if self.event_date:
            day_str = str(self.event_date.day)
            return day_str.lstrip('0') or '0'
        return ""
    
    @property
    def month(self):
        if self.event_date:
            return self.event_date.strftime('%b').upper()
        return ""
    
    @property
    def countdown_text(self):
        if not self.event_date:
            return "Date not set"
        
        try:
            today = timezone.now().date()
            delta = self.event_date - today
            days_remaining = delta.days
            
            if days_remaining < 0:
                return "Event has passed"
            elif days_remaining == 0:
                return "Starts today"
            elif days_remaining < 7:
                return f"Starts in {days_remaining} day{'s' if days_remaining > 1 else ''}"
            else:
                weeks = days_remaining // 7
                return f"Starts in {weeks} week{'s' if weeks > 1 else ''}"
        except:
            return "Date not set"


class About(models.Model):
    story_heading = models.CharField(max_length=200, default="Our Story")
    story_title = models.CharField(max_length=200, default="Educating Minds, Inspiring Hearts")
    story_content = models.TextField()
    story_image = models.ImageField(upload_to='media/website/', blank=True, null=True)
    
    mission_title = models.CharField(max_length=100, default="Our Mission")
    mission_content = models.TextField()
    
    vision_title = models.CharField(max_length=100, default="Our Vision")
    vision_content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "About"
    
    def __str__(self):
        return self.story_title


class TimelineItem(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='timeline_items')
    year = models.IntegerField()
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'year']
    
    def __str__(self):
        return f"{self.year} - {self.description[:50]}"


class CoreValue(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='core_values')
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Bootstrap icon class, e.g., bi bi-book")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class StudentsLife(models.Model):
    title = models.CharField(max_length=200, default="Student Life")
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='media/website/', blank=True, null=True)
    active_students_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Students Life"
        verbose_name_plural = "Students Life"

    def __str__(self):
        return self.title


class Activity(models.Model):
    students_life = models.ForeignKey(StudentsLife, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/website/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Statistic(models.Model):
    icon = models.CharField(max_length=100, help_text="Bootstrap icon class, e.g., bi bi-people")
    success_rate = models.IntegerField(default=87)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.title



class leadership(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    pics = models.ImageField(upload_to='media/about/')

    def __str__(self):
        return self.title


class Icon(models.Model):
    icon = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    leader = models.ForeignKey(leadership, related_name='leader', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text


class StudentLifeIntro(models.Model):
    """Model for the Vibrant Campus Experience intro section on student life page"""
    title = models.CharField(max_length=200, default="Vibrant Campus Experience")
    description_first = models.TextField(help_text="First paragraph of description")
    description_second = models.TextField(blank=True, help_text="Second paragraph of description")
    image = models.ImageField(upload_to='media/website/')
    button_text = models.CharField(max_length=100, default="Explore Campus")
    button_link = models.URLField(blank=True, help_text="URL for explore button")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Student Life Intro"
        verbose_name_plural = "Student Life Intro"
    
    def __str__(self):
        return self.title


class StudentOrganization(models.Model):
    """Model for student organizations and clubs"""
    title = models.CharField(max_length=200, default="Student Organizations & Clubs")
    icon = models.CharField(max_length=100, help_text="Bootstrap icon class, e.g., bi bi-music-note-beamed")
    name = models.CharField(max_length=150)
    description = models.TextField()
    badge_text = models.CharField(max_length=100, help_text="e.g., 15+ Groups")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class AthleticsProgram(models.Model):
    """Model for athletics and recreation programs"""
    title = models.CharField(max_length=200, default="Athletics & Recreation")
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='media/website/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class StudentLifeFacility(models.Model):
    """Model for campus facilities on student life page"""
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='media/website/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Student Life Facility"
        verbose_name_plural = "Student Life Facilities"
    
    def __str__(self):
        return self.name


class StudentSupportService(models.Model):
    """Model for student support services"""
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Bootstrap icon class, e.g., bi bi-heart-pulse")
    link = models.URLField(blank=True, help_text="URL for Learn More link")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class StudentLifeGalleryImage(models.Model):
    """Model for student life gallery images"""
    image = models.ImageField(upload_to='media/website/')
    title = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Student Life Gallery Image"
        verbose_name_plural = "Student Life Gallery Images"
    
    def __str__(self):
        return self.title or f"Image {self.id}"


class Testimonial(models.Model):
    """Model for student testimonials/reviews"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150, help_text="e.g., UX Designer, Software Engineer")
    description = models.TextField()
    image = models.ImageField(upload_to='media/website/', blank=True, null=True)
    rating = models.IntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.title}"