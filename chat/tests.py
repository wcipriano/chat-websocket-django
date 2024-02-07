import json

from asgiref.sync import sync_to_async
from asgiref.testing import ApplicationCommunicator
from channels.routing import URLRouter
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import re_path

from chat.consumers import ChatConsumer
from chat.models import Room


class ChatConsumerTest(TestCase):
    async def test_chat_message(self):
        # Create a user and a room
        room_name = 'sala1'
        user = await sync_to_async(User.objects.create_user)('testuser', 'password')
        await sync_to_async(Room.objects.get_or_create)(name=room_name)

        # Create a communicator (Used to simulate an ASGI requests to the application)
        application = URLRouter([
            re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi())
        ])
        communicator = ApplicationCommunicator(application, {
            "type": "websocket.connect",
            "path": f"/ws/chat/{room_name}/",
            "user": user
        })

        # Connect and test it
        await communicator.send_input({"type": "websocket.connect"})
        connected, _ = await communicator.receive_output(1)
        self.assertTrue(connected)

        # Receive the two messages that are sent when the user connects
        response = await communicator.receive_output(1)
        print(response)  # user_list

        response = await communicator.receive_output(1)
        print(response)  # user_join

        # Send a "hello" message
        await communicator.send_input({"type": "websocket.receive", "text": '{"message": "hello"}'})

        # Receive the message and assert the response
        response = await communicator.receive_output(1)
        print(response)
        self.assertEqual(json.loads(response["text"])['message'], "hello")

        # Closes the socket
        await communicator.send_input({"type": "websocket.disconnect", "code": 1000})
        await communicator.wait(1)  # Wait for the disconnect
