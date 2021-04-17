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
    

    def store_video(self, video_id, video):
        metadata = self.preprocessor.get_video_metadata(video)
        std_video = self.preprocessor.standardize_video_format(video)
        video_obj = self.preprocessor.split_chunks_video(std_video)
        iden = self.storage.store_video(video_id, metadata, video_obj)
        return iden
    
    def get_video(self, video_id):
        return {
            'video': self.storage.get_video(video_id),
            'metadata': self.storage.get_video_metadata(video_id)
        }
    
    def get_video_frame(self, video_id, frame):
        pass
    

 


    



