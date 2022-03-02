# chat/consumers.py
from django.contrib.auth import get_user_model

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from chat.models import ChatThread

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.groups = self.to_connect_groups()
        self.groups.append('main')
        print(self.groups)

        for group in self.groups:
            async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

        self.accept()

    # def disconnect(self, close_code):
    #     # Leave room group
    #     async_to_sync(self.channel_layer.group_discard)(
    #         self.room_group_name,
    #         self.channel_name
    #     )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        new_group = text_data_json.get('add_new_group', None)
        print(new_group)
        if new_group is not None: 
            self.groups.append(new_group)
            async_to_sync(self.channel_layer.group_add)(new_group, self.channel_name)
            async_to_sync(self.channel_layer.send)(self.channel_name,{
                'type': 'success_msg',
                'message': 'success'
            })
            # self.send(text_data=json.dumps({
            #     'message': 'success',
            # }))
        else:
            user_id = self.scope['user'].id
            other_user_id = text_data_json['send_msg_to']
            id1, id2 = f'chat_{user_id}_{other_user_id}', f'chat_{other_user_id}_{user_id}'
            if id1 in self.groups or id2 in self.groups:
                if id1 in self.groups:
                    group = id1
                elif id2 in self.groups:
                    group = id2

                message = text_data_json['message']

                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    group,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'chat_thread_id': group,
                    }
                )
            else:
                self.new_group_add(user_id, other_user_id)


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def success_msg(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def to_connect_groups(self):
        user = self.scope['user']
        print(user.id)
        threads = ChatThread.objects.by_user(user)
        chat_ids = []
        for thread in threads:
            chat_ids.append(thread.chat_group_name)
        return chat_ids

    def new_group_add(self, user_id, other_user_id):
        # _, user1, user2 = thread_id.split('_')
        first_user = get_user_model().objects.get(id=int(user_id))
        second_user = get_user_model().objects.get(id=int(other_user_id))
        new_chat_thread = ChatThread.objects.create(first=first_user, second=second_user)
        new_group_id = new_chat_thread.chat_group_name
        self.groups.append(new_group_id)
        print(new_group_id)
        async_to_sync(self.channel_layer.group_add)(new_group_id, self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            'main',
            {
                'type': 'new_thread_signal',
                'new_chat_thread': new_group_id,
            }
        )

    def new_thread_signal(self, event):
        self.send(text_data=json.dumps({
            'new_chat_thread': event['new_chat_thread']
        }))
        