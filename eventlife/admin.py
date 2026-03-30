from django.contrib import admin
from .models import *

class EventHilightInline(admin.TabularInline):
    model = EventHighlight
    extra = 1

class EventScheduleInline(admin.TabularInline):
    model = EventSchedule
    extra = 1

class EventGalleryInline(admin.TabularInline):
    model = EventGallery
    extra = 1

class EventOrganizerInline(admin.TabularInline):
    model = EventOrganizer
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'eventcategories', 'date', 'start_time', 'end_time', 'location', 'featured', 'participant_count', 'created_at')
    inlines = [EventHilightInline, EventScheduleInline, EventGalleryInline, EventOrganizerInline]
    list_filter = ('eventcategories', 'date', 'created_at', 'featured')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'image', 'eventcategories', 'featured')
        }),
        ('Date & Time', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        ('Location & Participants', {
            'fields': ('location', 'participant_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EventCategory)
class EventAdminCategory(admin.ModelAdmin):
    list_display  = ('text',)


@admin.register(EventLike)
class EventLikeAdmin(admin.ModelAdmin):
    list_display = ('event', 'created_at')
    list_filter = ('event', 'created_at')
    search_fields = ('event__title',)
    readonly_fields = ('created_at',)


@admin.register(EventRegistration)
class EventFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'student_type')
    readonly_fields = ('created_date',)
    fieldsets = (
        ('EventForm', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Other', {
            'fields': ('student_type','other_type')
        }),
        ('TimeStamp', {
            'fields': ('created_date',),
            'classes':('collapse')
        }),
    )

@admin.register(EventHighlight)
class EventHilightAdmin(admin.ModelAdmin):
    list_display = ('text',)
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        ('Highlight', {
            'fields': ('text', 'event')
        }),
        ('TimeStamp', {
            'fields': ('created_date', 'updated_date'),
            'classes':('collapse')
        }),
    )


@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'title', 'details', 'created_date')
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        ('Schedule', {
            'fields': ('title', 'details', 'events')
        }),
        ('Time', {
            'fields': ('start_time', 'end_time')
        }),
        ('TimeStamp', {
            'fields': ('created_date', 'updated_date'),
            'classes':('collapse')
        }),
    )


    
@admin.register(EventGallery)
class EventGalleryAdmin(admin.ModelAdmin):
    list_display = ('image', 'eventgallery', 'created_date')
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        ('Galllery', {
            'fields' : ('image', 'eventgallery')
        }),
        ('TimeStamp', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse')
        }),
    )


@admin.register(EventOrganizer)
class EventOrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_no', 'eventstaff')
    fieldsets = (
        ('Organizer Details', {     
            'fields': ('eventstaff', 'name', 'position', 'details', 'email', 'phone_no', 'image', 'event')
        }),
    )