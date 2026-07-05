from django.contrib import admin
from .models import Event, RSVP


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'location', 'is_active', 'created_at')
    list_filter = ('event_type', 'is_active', 'date')
    search_fields = ('title', 'organizer_name')
    readonly_fields = ('created_at',)


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('user', 'created_at')
