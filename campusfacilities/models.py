from django.db import models

# Create your models here.
class FacilityCategory(models.Model):
    """Categories for campus facilities"""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class (e.g., bi-book)")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Facility Categories"
    
    def __str__(self):
        return self.name


class CampusFacility(models.Model):
    """Campus facilities and amenities"""
    category = models.ForeignKey(FacilityCategory, on_delete=models.CASCADE, related_name='facilities')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/campus/facilities/')
    amenities = models.TextField(help_text="List amenities separated by newlines")
    location = models.CharField(max_length=200, blank=True)
    capacity = models.CharField(max_length=100, blank=True, help_text="e.g., 500+ students")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def amenities_list(self):
        """Return amenities as a list"""
        return [item.strip() for item in self.amenities.split('\n') if item.strip()]


class CampusHighlight(models.Model):
    """Featured campus highlights for the carousel"""
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('research', 'Research'),
        ('community', 'Community'),
        ('wellness', 'Wellness'),
        ('sports', 'Sports'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/campus/highlights/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    stat1_icon = models.CharField(max_length=50, help_text="Bootstrap icon class")
    stat1_text = models.CharField(max_length=100)
    stat2_icon = models.CharField(max_length=50, help_text="Bootstrap icon class")
    stat2_text = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title


class CampusInfo(models.Model):
    """General campus information"""
    title = models.CharField(max_length=200, default="Discover Our Modern Campus Facilities")
    description = models.TextField(default="Explore our state-of-the-art facilities designed for academic excellence and student success.")
    image = models.ImageField(upload_to='media/campus/')
    badge_text = models.CharField(max_length=100, default="Campus Excellence")
    buildings_count = models.CharField(max_length=50, default="95+")
    campus_acres = models.CharField(max_length=50, default="200")
    total_students = models.CharField(max_length=50, default="25k+")
    address = models.CharField(max_length=300)
    map_embed_url = models.URLField(help_text="Google Maps embed URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Campus Info"
    
    def __str__(self):
        return "Campus Information"


class CampusTour(models.Model):
    """Campus virtual tour information"""
    title = models.CharField(max_length=200, default="Take a Virtual Campus Tour")
    description = models.TextField(default="Cras ultricies ligula sed magna dictum porta. Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a. Vivamus suscipit tortor eget felis porttitor volutpat.")
    video = models.FileField(upload_to='media/campus/videos/', help_text="Upload tour video (MP4 format)")
    video_url = models.URLField(blank=True, help_text="Or provide video URL if not uploading")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Campus Tours"
    
    def __str__(self):
        return self.title


class TourFeature(models.Model):
    """Individual tour features"""
    tour = models.ForeignKey(CampusTour, on_delete=models.CASCADE, related_name='features')
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class (e.g., bi-binoculars)")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.tour.title} - {self.title}"