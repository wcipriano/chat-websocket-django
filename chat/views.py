# chat/views.py

from django.shortcuts import render
from chat.models import Room
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })


def send_test(request, room_name):
    print(f"Envia uma mensagem para todos os usuários do grupo chat_{room_name}")
    chat_room, created = Room.objects.get_or_create(name=room_name)

    msg = f"Msg tst auto. dt: {datetime.today().strftime('%Y-%d-%mT%H:%M:%S')}"
    user = request.user.username if request.user.is_authenticated else None
    channel_layer = get_channel_layer()
    message = dict(type='chat_message', message=msg, user=user, room=room_name)
    async_to_sync(channel_layer.group_send)(f'chat_{room_name}', message)

    return render(request, 'resp_messge.html', {
        'room': chat_room,
        'status_send': 1,
        'message': msg
    })
