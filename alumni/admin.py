from django.contrib import admin
from .models import Alumni, AlumniSuccess, AlumniNetwork, Campus


class AlumniSuccessInline(admin.TabularInline):
    """Inline admin for success stories within Alumni admin"""
    model = AlumniSuccess
    extra = 0
    fields = ('name', 'graduation_year', 'position', 'organization', 'is_featured', 'order')
    readonly_fields = ('name', 'graduation_year', 'position', 'organization')


@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'graduation_year', 'program', 'is_active')
    list_filter = ('graduation_year', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'program')
    inlines = [AlumniSuccessInline]
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'profile_image')
        }),
        ('Education', {
            'fields': ('graduation_year', 'program')
        }),
        ('Additional Information', {
            'fields': ('bio', 'linkedin_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(AlumniSuccess)
class AlumniSuccessAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'organization', 'graduation_year', 'is_featured', 'order')
    list_filter = ('is_featured', 'graduation_year', 'created_at')
    list_editable = ('order', 'is_featured')
    search_fields = ('name', 'position', 'organization')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'alumni', 'image')
        }),
        ('Professional Information', {
            'fields': ('position', 'organization', 'graduation_year')
        }),
        ('Story', {
            'fields': ('description', 'story_link')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order')
        }),
    )


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'is_active')
    list_filter = ('country', 'is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('name', 'country', 'city', 'address')
    fieldsets = (
        ('Campus Information', {
            'fields': ('name', 'country', 'city')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(AlumniNetwork)
class AlumniNetworkAdmin(admin.ModelAdmin):
    list_display = ('get_total_alumni', 'get_total_countries', 'get_years_of_excellence')
    readonly_fields = ('last_updated', 'get_total_alumni', 'get_total_countries', 'get_years_of_excellence', 'get_total_campuses')
    fieldsets = (
        ('Institution Founding', {
            'fields': ('founding_year',)
        }),
        ('Network Statistics (Auto-Calculated)', {
            'fields': ('get_total_alumni', 'get_total_countries', 'get_years_of_excellence', 'get_total_campuses'),
            'description': 'These values are automatically calculated based on your database records.'
        }),
        ('Additional Information', {
            'fields': ('description',)
        }),
        ('Metadata', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )
    
    def get_total_alumni(self, obj):
        return f"{obj.total_alumni_worldwide} (From completed student registrations)"
    get_total_alumni.short_description = "Total Alumni Worldwide"
    
    def get_total_countries(self, obj):
        return f"{obj.total_countries} countries"
    get_total_countries.short_description = "Countries with Campuses"
    
    def get_years_of_excellence(self, obj):
        return f"{obj.years_of_excellence}+ years"
    get_years_of_excellence.short_description = "Years of Excellence"
    
    def get_total_campuses(self, obj):
        return f"{obj.total_campuses} active campus locations"
    get_total_campuses.short_description = "Total Campuses"
