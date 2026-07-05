from django.db import models
from django.conf import settings
from django.utils import timezone


class JobPost(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50, choices=[
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('remote', 'Remote'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ])
    description = models.TextField()
    requirements = models.TextField(blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    application_email = models.EmailField(blank=True)
    application_link = models.URLField(blank=True, max_length=500)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], default='open')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company}"

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)
