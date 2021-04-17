from .storage import InMemoryStorage
from .preprocessor import VideoPreProcessor

class VideoVault():
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.storage = self._load_storage_driver()
        self.preprocessor = VideoPreProcessor()

    def _load_storage_driver(self):
        if self.config['storage'] == "memory":
            return InMemoryStorage()
        else:
            print("Storage driver not recognized")
    

    def store_video(self, video_id, metadata, video):
        videoObj = self.preprocessor.process_video(video, metadata)
        iden = self.storage.store_video(video_id, metadata, videoObj)
        return iden
    
    def get_video(self, video_id):
        return {
            'video': self.storage.get_video(video_id),
            'metadata': self.storage.get_video_metadata(video_id)
        }
    

 


    



