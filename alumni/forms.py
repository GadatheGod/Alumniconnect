from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image
import io
from .models import User, AlumniProfile
from django.conf import settings


class AlumniRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    department = forms.ChoiceField(choices=settings.DEPARTMENTS, required=True)
    year_of_passing = forms.IntegerField(required=True, min_value=1970, max_value=timezone.now().year)
    current_company = forms.CharField(max_length=200, required=False)
    current_role = forms.CharField(max_length=200, required=False)
    current_city = forms.CharField(max_length=100, required=False)
    native_location = forms.CharField(max_length=200, required=False)
    support_mode = forms.ChoiceField(choices=[
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('both', 'Both Online & Offline'),
        ('not_possible', 'Not Possible'),
    ], required=False)
    visit_frequency_coimbatore = forms.ChoiceField(choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('rarely', 'Rarely'),
        ('never', 'Never'),
    ], required=False)
    free_to_talk_days = forms.CharField(max_length=200, required=False)
    willing_to_mentor = forms.BooleanField(required=False)
    support_offered = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    profile_photo = forms.ImageField(required=False)

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError('Photo must be less than 5MB.')
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if photo.content_type not in allowed_types:
                raise ValidationError('Only JPG, PNG, and GIF formats are allowed.')
            img = Image.open(photo)
            if img.format == 'PNG':
                img = img.convert('RGB')
            max_size = (400, 400)
            img.thumbnail(max_size)
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=80, optimize=True)
            output.seek(0)
            filename = f'{photo.name.rsplit(".", 1)[0]}.jpg'
            photo = ContentFile(output.read(), name=filename)
        return photo

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('This phone number is already registered.')
        return phone


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)
    department = forms.ChoiceField(choices=settings.DEPARTMENTS, required=True)
    year_of_passing = forms.IntegerField(required=True, min_value=1970, max_value=timezone.now().year)
    current_company = forms.CharField(max_length=200, required=False)
    current_role = forms.CharField(max_length=200, required=False)
    current_city = forms.CharField(max_length=100, required=False)
    native_location = forms.CharField(max_length=200, required=False)
    support_mode = forms.ChoiceField(choices=[
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('both', 'Both Online & Offline'),
        ('not_possible', 'Not Possible'),
    ], required=False)
    visit_frequency_coimbatore = forms.ChoiceField(choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('rarely', 'Rarely'),
        ('never', 'Never'),
    ], required=False)
    free_to_talk_days = forms.CharField(max_length=200, required=False)
    willing_to_mentor = forms.BooleanField(required=False)
    support_offered = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    profile_photo = forms.ImageField(required=False)

    def __init__(self, *args, profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if AlumniProfile.objects.filter(phone=phone).exclude(id=self.profile.id).exists():
            raise forms.ValidationError('This phone number is already registered.')
        return phone

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError('Photo must be less than 5MB.')
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if photo.content_type not in allowed_types:
                raise ValidationError('Only JPG, PNG, and GIF formats are allowed.')
            img = Image.open(photo)
            if img.format == 'PNG':
                img = img.convert('RGB')
            max_size = (400, 400)
            img.thumbnail(max_size)
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=80, optimize=True)
            output.seek(0)
            filename = f'{photo.name.rsplit(".", 1)[0]}.jpg'
            photo = ContentFile(output.read(), name=filename)
        return photo
