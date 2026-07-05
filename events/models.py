from django.db import models
from django.conf import settings
from django.utils import timezone


class Event(models.Model):
    event_type = models.CharField(max_length=50, choices=[
        ('reunion', 'Batch Reunion'),
        ('webinar', 'Webinar'),
        ('meetup', 'Meetup'),
        ('guest_lecture', 'Guest Lecture'),
        ('alumni_day', 'Alumni Day'),
        ('other', 'Other'),
    ])
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=300, blank=True)
    organizer_name = models.CharField(max_length=200)
    organizer_email = models.EmailField(blank=True)
    max_attendees = models.IntegerField(default=0, help_text='0 for unlimited')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d %b %Y')}"

    @property
    def is_past(self):
        return timezone.now() > self.date

    @property
    def available_slots(self):
        if self.max_attendees == 0:
            return 999999
        return max(0, self.max_attendees - self.rsvp.filter(status='confirmed').count())

    @property
    def is_full(self):
        return self.available_slots == 0


class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvp')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ], default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user} -> {self.event}"
