from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Job, Application, Resume

# Register Resume directly
admin.site.register(Resume)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'status_badge', 'posted_at', 'action_links')
    search_fields = ('title', 'location', 'description')
    list_filter = ('location', 'posted_at')
    ordering = ('-posted_at',)
    list_per_page = 20
    readonly_fields = ('posted_at',)

    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'description', 'location', 'salary_range')
        }),
        ('Job Details', {
            'fields': ('requirements', 'is_active', 'posted_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 4px;">Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 4px;">Inactive</span>')

    status_badge.short_description = 'Status'

    def action_links(self, obj):
        return format_html(
            '<a class="button" href="{}">Edit</a>',
            reverse('admin:resume_job_change', args=[obj.pk])
        )
    action_links.short_description = 'Actions'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'status_badge', 'resume_download', 'applied_at', 'action_links')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'user__email', 'job__title')
    ordering = ('-applied_at',)
    list_per_page = 20
    readonly_fields = ('applied_at',)

    fieldsets = (
        ('Application Info', {
            'fields': ('user', 'job', 'status')
        }),
        ('Timeline', {
            'fields': ('applied_at',),
            'classes': ('collapse',)
        }),
    )

    def job_title(self, obj):
        return obj.job.title if obj.job else '-'
    job_title.short_description = 'Job Title'

    def status_badge(self, obj):
        status_colors = {
            'pending': '#ffc107',
            'accepted': '#28a745',
            'rejected': '#dc3545',
            'reviewed': '#17a2b8',
        }
        color = status_colors.get(obj.status.lower(), '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px;">{}</span>',
            color, obj.status.title()
        )
    status_badge.short_description = 'Status'

    def resume_download(self, obj):
        if obj.resume:
            return format_html('<a href="{}" download>Download</a>', obj.resume.url)
        return '-'
    resume_download.short_description = 'Resume'

    def action_links(self, obj):
        return format_html(
            '<a class="button" href="{}">Edit</a>',
            reverse('admin:resume_application_change', args=[obj.pk])
        )
    action_links.short_description = 'Actions'


# Admin branding
admin.site.site_header = "Resume Management System"
admin.site.site_title = "RMS Admin"
admin.site.index_title = "Welcome to Resume Management Admin"
