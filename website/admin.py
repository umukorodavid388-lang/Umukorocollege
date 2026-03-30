from django.contrib import admin
from .models import *

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1

class TimelineItemInline(admin.TabularInline):
    model = TimelineItem
    extra = 1
    fields = ('year', 'description', 'order')

class CoreValueInline(admin.TabularInline):
    model = CoreValue
    extra = 1
    fields = ('name', 'description', 'icon', 'order')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'picture')
    inlines = [FeatureInline]

@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'countdown_text')
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'content', 'event_date')
        }),
        ('Action', {
            'fields': ('rsvp_url',)
        }),
        ('Relations', {
            'fields': ('hero',)
        })
    )
    readonly_fields = ('countdown_text',)
    
    def countdown_text(self, obj):
        return obj.countdown_text
    countdown_text.short_description = "Countdown"


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('story_title', 'mission_title', 'vision_title')
    fieldsets = (
        ('Story Section', {
            'fields': ('story_heading', 'story_title', 'story_content', 'story_image')
        }),
        ('Mission', {
            'fields': ('mission_title', 'mission_content')
        }),
        ('Vision', {
            'fields': ('vision_title', 'vision_content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TimelineItemInline, CoreValueInline]


@admin.register(TimelineItem)
class TimelineItemAdmin(admin.ModelAdmin):
    list_display = ('year', 'about', 'order')
    list_filter = ('about', 'year')
    ordering = ('about', 'order')


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', 'icon', 'order')
    list_filter = ('about',)
    ordering = ('about', 'order')


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1


@admin.register(StudentsLife)
class StudentsLifeAdmin(admin.ModelAdmin):
    list_display = ('title', 'active_students_count', 'created_at')
    inlines = [ActivityInline]


@admin.register(StudentLifeIntro)
class StudentLifeIntroAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description_first', 'description_second')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Button', {
            'fields': ('button_text', 'button_link')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StudentOrganization)
class StudentOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'badge_text', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Organization Details', {
            'fields': ('name', 'description', 'badge_text')
        }),
        ('Display Settings', {
            'fields': ('icon', 'order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order',)


@admin.register(AthleticsProgram)
class AthleticsProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Program Details', {
            'fields': ('name', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order',)


@admin.register(StudentLifeFacility)
class StudentLifeFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Facility Details', {
            'fields': ('name', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order',)


@admin.register(StudentSupportService)
class StudentSupportServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    fieldsets = (
        ('Service Details', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Link', {
            'fields': ('link',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order',)


@admin.register(StudentLifeGalleryImage)
class StudentLifeGalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    fieldsets = (
        ('Image', {
            'fields': ('image', 'title')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'students_life', 'order')
    list_filter = ('students_life',)

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'description', 'success_rate')
    fieldsets = (
        (None, {
            'fields': ('icon', 'success_rate', 'title', 'description')
        }),
    )
    
    def has_add_permission(self, request):
        # Only one statistic record allowed
        return not Statistic.objects.exists()

class IconIlines(admin.TabularInline):
    model = Icon
    extra = 1



@admin.register(leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('title', 'description' )    
    inlines = [IconIlines]

@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ('icon', 'text', 'content')
    fieldsets = (
        (None, {
            'fields': ('icon', 'text', 'content')
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'rating', 'is_active', 'order', 'created_at')
    list_editable = ('is_active', 'order')
    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('name', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'title', 'image')
        }),
        ('Testimonial', {
            'fields': ('description', 'rating')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('order', '-created_at')