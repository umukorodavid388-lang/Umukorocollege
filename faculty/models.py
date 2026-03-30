from django.db import models

# Create your models here.
class StaffCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Staff(models.Model):
    picture = models.ImageField(upload_to='media/staff/', blank=True)
    name = models.CharField(max_length=100, blank=True)
    work_tile = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    category = models.ForeignKey(StaffCategory, related_name='staff_members', on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.name