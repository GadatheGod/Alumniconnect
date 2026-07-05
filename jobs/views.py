from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from .models import JobPost
from .forms import JobPostForm


def job_list(request):
    jobs = JobPost.objects.filter(is_active=True).select_related('posted_by')

    search = request.GET.get('search', '')
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(company__icontains=search) |
            Q(description__icontains=search)
        )
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, 'jobs/job_list.html', {'jobs': jobs})


@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST, posted_by=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = JobPostForm()

    return render(request, 'jobs/job_create.html', {'form': form})


def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, is_active=True)
    return render(request, 'jobs/job_detail.html', {'job': job})


@login_required
@require_POST
def toggle_job_status(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    user = request.user
    
    if user == job.posted_by or user.is_staff:
        if job.status == 'open':
            job.status = 'closed'
            messages.success(request, 'Job marked as closed.')
        else:
            job.status = 'open'
            messages.success(request, 'Job marked as open.')
        job.save()
    else:
        messages.error(request, 'You do not have permission to change this job status.')
    
    return redirect('job_detail', job_id=job_id)
