from django.contrib import admin
from .models import *


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
	list_display = ('title', 'degree_type', 'duration', 'is_featured', 'order', 'created_at')
	list_filter = ('degree_type', 'is_featured')
	search_fields = ('title', 'description')
	ordering = ('order', '-created_at')


admin.site.register(ProgramIntrest)


