from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    room_type = models.CharField(max_length=10, choices=[
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'),
    ], default='direct')

    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='ChatRoomMember', related_name='chat_rooms'
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.room_type == 'direct':
            member_names = list(self.members.values_list('username', flat=True))
            return f"Chat: {' - '.join(member_names)}"
        return self.name or "Group Chat"

    @property
    def latest_message(self):
        return self.messages.first() if self.messages.exists() else None

    @property
    def other_member(self):
        if self.room_type != 'direct':
            return None
        members = list(self.members.all())
        if len(members) >= 2:
            return [m for m in members if m.id != members[0].id][0]
        return members[0] if members else None

    def get_room_id(self):
        if self.room_type == 'direct':
            members = sorted([str(m.id) for m in self.members.all()])
            return f"direct_{members[0]}_{members[1]}"
        return f"group_{self.id}"


class ChatRoomMember(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='room_members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ['room', 'user']

    def __str__(self):
        return f"{self.user} in {self.room}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"
