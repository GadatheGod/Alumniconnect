from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AlumniProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'phone', 'date_joined')
    list_filter = ('date_joined',)
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Alumni Info', {'fields': ('phone',)}),
    )


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'department', 'year_of_passing', 'current_company', 'created_at')
    list_filter = ('department', 'year_of_passing')
    search_fields = ('first_name', 'last_name', 'phone', 'current_company', 'department', 'email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Personal Info', {'fields': ('user', 'first_name', 'last_name', 'email', 'phone', 'department', 'year_of_passing')}),
        ('Career', {'fields': ('current_company', 'current_role')}),
        ('Location', {'fields': ('current_city',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )

    def display_name(self, obj):
        return obj.full_name
    display_name.short_description = 'Name'
