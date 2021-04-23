from .storage import InMemoryStorage, RedisStorage
from .processor import VideoProcessor
import joblib
import threading

class VideoVault():
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.storage = self._load_storage_driver()
        self.processor = VideoProcessor()


    def _load_storage_driver(self):
        if self.config['storage'] == "memory":
            return InMemoryStorage()
        if self.config['storage'] == "redis":
            return RedisStorage()
        else:
            print("Storage driver not recognized")
    

    def store_video(self, video_id, video):
        metadata = self.processor.get_video_metadata(video)
        print(metadata)
        std_video = self.processor.standardize_video_format(video, metadata['codec_name'])
        print("Standardized video")
        print(self.processor.get_video_metadata(std_video))
        video_obj = self.processor.split_chunks_video(std_video)
        print("Done splitting video into chunks", video_obj.get_num_frames())
        iden = self.storage.store_video(video_id, metadata, video_obj)
        print("Done persisting chunks to storage")
        return iden
    

    def get_video(self, video_id):
        return {
            'video': self.storage.get_video(video_id),
            'metadata': self.storage.get_video_metadata(video_id)
        }
    
    def get_every_nth_video_frame(self, video_id, n):
        metadata = self.storage.get_video_metadata(video_id)
        frames = []
        for framenum in range(1, int(metadata['nb_frames'])+1, n):
            print("Processing Frame:", str(framenum))
            chunk, startframe = self.storage.get_chunk_with_frame(video_id, framenum)
            frame = self.processor.get_frame_from_video(chunk, framenum-startframe)
            frames.append(frame)
        return frames
    
    def get_every_nth_video_frame_threaded(self, video_id, n):
        metadata = self.storage.get_video_metadata(video_id)

        def getFrame(framenum, video_id, processor, storage):
            chunk, startframe = storage.get_chunk_with_frame(video_id, framenum)
            frame = processor.get_frame_from_video(chunk, framenum-startframe)
            return frame
        
        parallelize = joblib.Parallel(n_jobs=10, backend='threading')
        frames = parallelize(
                    joblib.delayed(getFrame)(
                        framenum, video_id, self.processor, self.storage
                    ) for framenum in range(1, int(metadata['nb_frames'])+1, n)
                )
        return frames
        

