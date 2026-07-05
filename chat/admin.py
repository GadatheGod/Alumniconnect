from django.contrib import admin
from .models import ChatRoom, ChatRoomMember, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'room_type', 'created_by', 'updated_at')
    list_filter = ('room_type',)
    search_fields = ('name',)


@admin.register(ChatRoomMember)
class ChatRoomMemberAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'is_admin')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'content_preview', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('sender', 'created_at')

    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = 'Message'
