from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import ChatRoom, Message
from alumni.models import User


@login_required
def chat_list(request):
    rooms = ChatRoom.objects.filter(members=request.user).order_by('-updated_at')
    return render(request, 'chat/chat_list.html', {'rooms': rooms})


@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id, members=request.user)
    messages_list = room.messages.all()[:50]

    for msg in messages_list:
        msg.is_read = True
        msg.save(update_fields=['is_read'])

    context = {
        'room': room,
        'messages': messages_list,
    }
    return render(request, 'chat/chat_room.html', context)


@login_required
@require_POST
def create_direct_chat(request, user_id):
    if user_id == request.user.id:
        return JsonResponse({'success': False, 'message': 'Cannot chat with yourself.'})

    target_user = get_object_or_404(User, id=user_id)

    existing_room = ChatRoom.objects.filter(
        room_type='direct',
        members=request.user
    ).filter(members=target_user).first()

    if existing_room:
        return JsonResponse({'success': True, 'redirect': f'/chat/room/{existing_room.id}/'})

    room = ChatRoom.objects.create(room_type='direct', created_by=request.user)
    room.members.add(request.user, target_user)

    return JsonResponse({'success': True, 'redirect': f'/chat/room/{room.id}/'})


@login_required
@require_POST
def create_group_chat(request):
    name = request.POST.get('name', '')
    member_ids = request.POST.getlist('members')

    if not name:
        return JsonResponse({'success': False, 'message': 'Group name is required.'})

    room = ChatRoom.objects.create(room_type='group', name=name, created_by=request.user)
    room.members.add(request.user)

    for member_id in member_ids:
        try:
            user = User.objects.get(id=member_id)
            if user != request.user:
                room.members.add(user)
        except User.DoesNotExist:
            pass

    return JsonResponse({'success': True, 'redirect': f'/chat/room/{room.id}/'})
