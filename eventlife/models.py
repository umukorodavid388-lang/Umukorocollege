from django.db import models
from django.contrib.auth.models import User
from faculty.models import *
from faculty.models import *



class EventCategory(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text

class Event(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/events/')
    date = models.DateTimeField()
    eventcategories = models.ForeignKey(EventCategory, related_name='event', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    featured = models.BooleanField(default=False)
    location = models.CharField(max_length=300)
    participant_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_day(self):
        return self.date.strftime('%d')
    
    def get_month(self):
        return self.date.strftime('%b').upper()
    
    def get_category_display_lower(self):
        return self.get_eventcategories_display().lower()
    
    def get_likes_count(self):
        return self.likes.count()
    
    def get_shares_count(self):
        return self.shares.count()


class EventLike(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event',)
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Like on {self.event.title}"


class EventShare(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='shares')
    shared_to = models.CharField(
        max_length=50,
        choices=[
            ('facebook', 'Facebook'),
            ('twitter', 'Twitter'),
            ('whatsapp', 'WhatsApp'),
            ('email', 'Email'),
            ('copy_link', 'Copy Link'),
        ],
        default='copy_link'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Shared {self.event.title} to {self.get_shared_to_display()}"
    

class EventHighlight(models.Model):
    text = models.CharField(max_length=100)
    event = models.ForeignKey(Event, related_name='highlight', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    

class EventSchedule(models.Model):
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    title = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    events = models.ForeignKey(Event, related_name='schedule', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title
    
class EventGallery(models.Model):
    image = models.ImageField(upload_to='media/event/gallery')
    eventgallery = models.ForeignKey(Event, related_name='eventgallery', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)  



    class Meta:
        ordering = ['-created_date']


class EventRegistration(models.Model):

    STUDENT_TYPE_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    student_type = models.CharField(
        max_length=20,
        choices=STUDENT_TYPE_CHOICES
    )
    other_type = models.CharField(
        max_length=100,
        blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class EventOrganizer(models.Model):
    event = models.ForeignKey(Event, related_name='eventorganizer', on_delete=models.CASCADE, blank=True, null=True)
    eventstaff = models.ForeignKey(Staff, related_name='eventstaff', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='media/event/', blank=True)
    name = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=200, blank=True)
    details = models.TextField(blank=True)
    email = models.EmailField(unique=True, blank=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.eventstaff:
            return f'{self.eventstaff.name} - {self.name}'
        return self.name
    