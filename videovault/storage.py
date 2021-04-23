
from abc import ABC, abstractmethod

class VideoStorage(ABC):
    def __init__(self):
        super().__init__()
        self.on_init()

    @abstractmethod
    def on_init(self):
        pass

    @abstractmethod
    def store_video(self, video_id, metadata, video):
        pass

    @abstractmethod
    def get_video(self, video_id):
        pass

    @abstractmethod
    def get_video_metadata(self, video_id):
        pass

    @abstractmethod
    def get_chunk_with_frame(self, video_id, framenum):
        pass



class InMemoryStorage(VideoStorage):
    def on_init(self):
        self.video_store = {}
        self.metadata_store = {}

    def store_video(self, video_id, metadata, video):
        self.video_store[video_id] = video
        self.metadata_store[video_id] = metadata
        return video_id
    
    def get_video(self, video_id):
        return self.video_store[video_id]

    def get_video_metadata(self, video_id):
        return self.metadata_store[video_id]
    
    def get_chunk_with_frame(self, video_id, framenum):
        raise Exception("Not Implemented")


import redis
import json

class RedisStorage(VideoStorage):
    def on_init(self):
        self.redis = redis.Redis(host='localhost', port=6379)
    

    def store_video(self, video_id, metadata, video):
        d = {}
        for chunk in video.get_chunks():
            d[chunk.get_bytes()] = chunk.get_start_frame()
        self.redis.zremrangebyscore('video_chunk::'+str(video_id), '-inf', '+inf')
        self.redis.zadd('video_chunk::'+str(video_id), d)
        self.redis.set('video_metadata::'+str(video_id), json.dumps(metadata))
        return video_id
    
    def get_video(self, video_id):
        raise Exception("Not Implemented")

    def get_video_metadata(self, video_id):
        return json.loads(self.redis.get('video_metadata::'+str(video_id)))
    
    def get_chunk_with_frame(self, video_id, framenum):
        res = self.redis.zrevrangebyscore('video_chunk::'+str(video_id), int(framenum), '-inf', start=0, num=1, withscores=True)
        if not res:
            return None
        return res[0][0], int(res[0][1])
    
    

    

        
