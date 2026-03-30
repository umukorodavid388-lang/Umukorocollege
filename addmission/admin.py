from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_email', 'program', 'status', 'is_passed', 'enrollment_date')
    list_editable = ('status', 'is_passed')
    list_filter = ('status', 'is_passed', 'program', 'enrollment_date')
    search_fields = ('student_name', 'student_email', 'program__title')
    readonly_fields = ('enrollment_date', 'created_at', 'updated_at')
    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'student_email', 'student_phone', 'pics')
        }),
        ('Program & Status', {
            'fields': ('program', 'status', 'is_passed', 'grades')
        }),
        ('Dates', {
            'fields': ('enrollment_date', 'completion_date', 'created_at', 'updated_at')
        }),
        ('Additional Notes', {
            'fields': ('notes',)
        }),
    )


@admin.register(ApplicationStep)
class ApplicationStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('step_number',)


@admin.register(AdmissionRequirement)
class AdmissionRequirementAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'is_mandatory', 'is_active', 'order')
    list_editable = ('is_mandatory', 'is_active', 'order')
    list_filter = ('is_mandatory', 'is_active')
    search_fields = ('requirement', 'description')
    ordering = ('order',)


@admin.register(TuitionProgram)
class TuitionProgramAdmin(admin.ModelAdmin):
    list_display = ('program_name', 'tuition_per_year', 'fees', 'total_per_year', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('program_name',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Program Information', {
            'fields': ('program_name', 'description')
        }),
        ('Fees & Tuition', {
            'fields': ('tuition_per_year', 'fees')
        }), 
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdmissionDeadline)
class AdmissionDeadlineAdmin(admin.ModelAdmin):
    list_display = ('deadline_name', 'deadline_date', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'deadline_date')
    search_fields = ('deadline_name', 'description')
    ordering = ('order', 'deadline_date')


@admin.register(InformationRequest)
class InformationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'program', 'status', 'is_contacted', 'created_at')
    list_editable = ('status', 'is_contacted')
    list_filter = ('status', 'is_contacted', 'program', 'created_at')
    search_fields = ('name', 'email', 'phone', 'program')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Interest', {
            'fields': ('program', 'message')
        }),
        ('Status', {
            'fields': ('status', 'is_contacted')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CampusVisitRequest)
class CampusVisitRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'preferred_date', 'visit_type', 'is_confirmed', 'created_at')
    list_editable = ('is_confirmed',)
    list_filter = ('visit_type', 'is_confirmed', 'preferred_date', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Visitor Information', {
            'fields': ('name', 'email', 'phone', 'number_of_visitors')
        }),
        ('Visit Details', {
            'fields': ('visit_type', 'preferred_date', 'preferred_time', 'special_requests')
        }),
        ('Status', {
            'fields': ('is_confirmed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )



admin.site.register(TutionNote)


class CampusVisitContentInline(admin.TabularInline):
    model = CampusVisitContent
    extra = 1


@admin.register(CampusVisst)
class CampusVisstAdmin(admin.ModelAdmin):  
    inlines = [CampusVisitContentInline]  
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    fieldsets = (
        ('Campus Visit', {
            'fields': ('picture','title', 'content','details')
        }),
    )


@admin.register(CampusVisitContent)
class CampusVisitContentAdmin(admin.ModelAdmin):    
    list_display = ('text',)