from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Event, RSVP
from .forms import EventForm


def event_list(request):
    events = Event.objects.filter(is_active=True)

    search = request.GET.get('search', '')
    event_type = request.GET.get('event_type', '')

    if search:
        events = events.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(organizer_name__icontains=search)
        )
    if event_type:
        events = events.filter(event_type=event_type)

    return render(request, 'events/event_list.html', {'events': events})


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, created_by=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = EventForm()

    return render(request, 'events/event_create.html', {'form': form})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    rsvps = event.rsvp.filter(status='confirmed')
    user_rsvp = None

    if request.user.is_authenticated:
        user_rsvp = RSVP.objects.filter(event=event, user=request.user).first()

    context = {
        'event': event,
        'rsvps': rsvps,
        'user_rsvp': user_rsvp,
        'available_slots': event.available_slots,
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def event_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.is_past:
        messages.error(request, 'This event has passed.')
        return redirect('event_detail', event_id=event_id)

    if event.is_full:
        messages.error(request, 'This event is full.')
        return redirect('event_detail', event_id=event_id)

    rsvp, created = RSVP.objects.get_or_create(
        event=event,
        user=request.user,
        defaults={'status': 'confirmed'}
    )

    if not created:
        if rsvp.status == 'confirmed':
            rsvp.status = 'cancelled'
        else:
            rsvp.status = 'confirmed'
        rsvp.save()
        messages.info(request, f'Your RSVP has been {rsvp.status}.')
    else:
        messages.success(request, 'You have RSVP\'d successfully!')

    return redirect('event_detail', event_id=event_id)
