from django import forms
from .models import JobPost


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'company', 'location', 'job_type', 'description',
                  'requirements', 'salary_range', 'application_email', 'application_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, posted_by=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.posted_by = posted_by

    def save(self, *args, **kwargs):
        kwargs['commit'] = kwargs.get('commit', True)
        job = super().save(*args, **kwargs)
        if self.posted_by:
            job.posted_by = self.posted_by
            if not kwargs.get('commit'):
                job.save()
        return job
