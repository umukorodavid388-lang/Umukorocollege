from django.db import models
from addmission.models import *

# Create your models here.

class Category(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text
    

class News(models.Model):
    picture = models.ImageField(upload_to='media/news/')
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(StudentRegistration, related_name='user', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Display as main featured program")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)  
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
