from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_type', 'title', 'description', 'date', 'location',
                  'organizer_name', 'organizer_email', 'max_attendees']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, created_by=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_by = created_by

    def save(self, *args, **kwargs):
        kwargs['commit'] = kwargs.get('commit', True)
        event = super().save(*args, **kwargs)
        if self.created_by:
            event.created_by = self.created_by
            if not kwargs.get('commit'):
                event.save()
        return event
