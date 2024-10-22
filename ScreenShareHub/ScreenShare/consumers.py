from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LiveStreamConsumer(AsyncWebsocketConsumer):
    connected_clients = set()

    async def connect(self):
        self.connected_clients.add(self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        self.connected_clients.remove(self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'videoTrack':
            for client in self.connected_clients:
                if client != self.channel_name:
                    await self.send_video_track(client, data['trackId'])
        elif data['type'] == 'trackEnded':
            for client in self.connected_clients:
                await self.send_track_ended(client, data['trackId'])

    async def send_video_track(self, client, track_id):
        await self.channel_layer.send(client, {
            'type': 'video.track',
            'trackId': track_id,
        })

    async def send_track_ended(self, client, track_id):
        await self.channel_layer.send(client, {
            'type': 'trackEnded',
            'trackId': track_id,
        })
