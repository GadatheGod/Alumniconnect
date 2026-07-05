import uuid
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.email or self.username


class OTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'

    def __str__(self):
        return f'{self.email} - {self.code}'

    def is_valid(self):
        if timezone.now() - self.created_at > timedelta(minutes=10):
            self.delete()
            return False
        return True

    @classmethod
    def generate(cls, email):
        cls.objects.filter(email=email).delete()
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return cls.objects.create(email=email, code=code)


class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_profile')
    email = models.EmailField(unique=True, blank=True, null=True)

    # Basic info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=10, choices=settings.DEPARTMENTS)
    year_of_passing = models.IntegerField(
        help_text='E.g., 2015'
    )

    # Career
    current_company = models.CharField(max_length=200, blank=True)
    current_role = models.CharField(max_length=200, blank=True)

    # Location
    current_city = models.CharField(max_length=100, blank=True)
    native_location = models.CharField(max_length=200, blank=True)

    # Profession
    support_mode = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            ('online', 'Online'),
            ('offline', 'Offline'),
            ('both', 'Both Online & Offline'),
            ('not_possible', 'Not Possible'),
        ],
        help_text='Mode of support — Online, Offline, Both, or Not Possible',
    )

    # Connectivity
    visit_frequency_coimbatore = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
            ('rarely', 'Rarely'),
            ('never', 'Never'),
        ],
    )
    free_to_talk_days = models.CharField(max_length=200, blank=True, help_text='e.g., Weekends, Monday-Friday evenings')

    # Networking
    willing_to_mentor = models.BooleanField(default=False, help_text='Willing to associate and support batchmates through networks')
    support_offered = models.TextField(blank=True, help_text='Area of experience, networks, market, etc.')

    # Photo
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year_of_passing']
        indexes = [
            models.Index(fields=['department', 'year_of_passing']),
            models.Index(fields=['current_company']),
            models.Index(fields=['first_name', 'last_name']),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.department} {self.year_of_passing}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def display_name(self):
        return self.full_name or self.user.get_full_name() or self.user.username

    def save(self, *args, **kwargs):
        if self.email is None and self.user and self.user.email:
            self.email = self.user.email
        if self.user:
            if not self.user.first_name or self.user.first_name == '':
                parts = self.full_name.split(' ', 1)
                self.user.first_name = parts[0]
                if len(parts) > 1:
                    self.user.last_name = parts[1]
                self.user.save()
        super().save(*args, **kwargs)



