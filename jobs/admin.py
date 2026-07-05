from django.contrib import admin
from .models import JobPost


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'posted_by', 'is_active', 'created_at')
    list_filter = ('job_type', 'is_active', 'created_at')
    search_fields = ('title', 'company', 'location')
    readonly_fields = ('posted_by', 'created_at')
    list_editable = ('is_active',)
