
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
    def get_frame(self, video_id, framenum):
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
    
    def get_frame(self, video_id, framenum):
        raise Exception("Not Implemented")
    
    

    

        
