import json
from channels.generic.websocket import AsyncWebsocketConsumer
import docker
import asyncio;
import threading;

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

docker_ips = ["192.168.2.77","192.168.2.78"]
docker_image = "centos:7.9.2009"
docker_port = 2375

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        nickname = text_data_json['nickname']
        

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'nickname': nickname,
            }
        )


    # Receive message from room group
    async def chat_message(self, event):
        message =  event['message']
        nickname =  event['nickname']

        for i in docker_ips:
            new_loop = asyncio.new_event_loop()                       
            t = threading.Thread(target=start_loop,args=(new_loop,))  
            t.start()
            run_func = self.connect_docker(i,docker_port,docker_image)
            asyncio.run_coroutine_threadsafe(run_func,new_loop)


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'nickname': nickname,
        }))




    
    async def connect_docker(self,ip,port=2375,image=""):
        client = None;
        try:
            client = docker.DockerClient(base_url=f'tcp://{ip}:{port}',timeout=3)
            #print(client);
            #print(client.images.list());
            #client.images.pull(image);
            #client.close();
            client.images.pull(image);
        except Exception as e:
            print(e);

    
