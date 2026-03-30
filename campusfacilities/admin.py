from django.contrib import admin
from .models import FacilityCategory, CampusFacility, CampusHighlight, CampusInfo, CampusTour, TourFeature

# Register your models here.

@admin.register(FacilityCategory)
class FacilityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('name',)
    ordering = ('order',)


@admin.register(CampusFacility)
class CampusFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_featured', 'order', 'created_at')
    list_editable = ('order', 'is_featured')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('order', '-created_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Details', {
            'fields': ('location', 'capacity', 'amenities')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CampusHighlight)
class CampusHighlightAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('order', '-created_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Statistics', {
            'fields': ('stat1_icon', 'stat1_text', 'stat2_icon', 'stat2_text')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CampusInfo)
class CampusInfoAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fieldsets = (
        ('Header Information', {
            'fields': ('title', 'description', 'badge_text')
        }),
        ('Campus Statistics', {
            'fields': ('buildings_count', 'campus_acres', 'total_students')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Map & Location', {
            'fields': ('address', 'map_embed_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

class TourFeatureInline(admin.TabularInline):
    """Inline admin for tour features"""
    model = TourFeature
    extra = 1
    fields = ('icon', 'title', 'description', 'order')
    ordering = ('order',)


@admin.register(CampusTour)
class CampusTourAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    inlines = [TourFeatureInline]
    fieldsets = (
        ('Tour Information', {
            'fields': ('title', 'description')
        }),
        ('Media', {
            'fields': ('video', 'video_url'),
            'description': 'Upload video file (MP4 format) or provide video URL'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TourFeature)
class TourFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'tour', 'order')
    list_editable = ('order',)
    list_filter = ('tour',)
    search_fields = ('title', 'description')
    ordering = ('order',)