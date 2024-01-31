# chat/consumers.py

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Room, Message


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.room_general = 'geral'
        self.room_general_group = f'chat_{self.room_general}'
        self.user_inbox = None

    def join_groups(self):
        # join the room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        print(f"connected: {f'user: {self.user.username},' if self.user.is_authenticated else ''}  "
              f"room: {self.room_name}, channel: {self.channel_name}")
        # join the user inbox group
        async_to_sync(self.channel_layer.group_add)(self.user_inbox, self.channel_name)

    def left_groups(self):
        # left the room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        print(f"disconected: {f'user: {self.user.username},' if self.user.is_authenticated else ''}  "
              f"room: {self.room_name}, channel: {self.channel_name}")
        # left the user inbox group
        async_to_sync(self.channel_layer.group_discard)(self.user_inbox, self.channel_name)

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope['user']
        self.user_inbox = f'inbox_{self.user.username}'

        # connection has to be accepted
        self.accept()

        # Join the groups
        self.join_groups()

        # send the user list to the newly joined user
        self.send(json.dumps({
            'type': 'user_list',
            'users': [user.username for user in self.room.online.all()],
        }))

        if self.user.is_authenticated:
            self.room.online.add(self.user)
            message = dict(type="user_join", room=self.room_name, user=self.user.username)
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, message)
            if self.room_name != self.room_general:
                async_to_sync(self.channel_layer.group_send)(self.room_general_group, message)

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            self.room.online.remove(self.user)
            message = dict(type="user_leave", room=self.room_name, user=self.user.username)
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, message)
            if self.room_name != self.room_general:
                async_to_sync(self.channel_layer.group_send)(self.room_general_group, message)

        # Left the groups
        self.left_groups()

    def receive(self, text_data=None, bytes_data=None):
        if not self.user.is_authenticated:
            return

        json_data = json.loads(text_data)
        msg_txt = json_data['message']

        # Private or group message?
        if json_data.get('to'):
            group = f'inbox_{json_data["to"]}'
            type_msg = 'private_message'
        else:
            group = self.room_group_name
            type_msg = "chat_message"

        message = dict(type=type_msg, message=msg_txt, user=self.user.username, room=self.room_name)
        async_to_sync(self.channel_layer.group_send)(group, message)
        Message.objects.create(user=self.user, room=self.room, content=message)
        if self.room_name != self.room_general and not json_data.get('to'):
            async_to_sync(self.channel_layer.group_send)(self.room_general_group, message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

