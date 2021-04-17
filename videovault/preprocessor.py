from .video import VideoObject
from .videochunk import VideoChunkObject

class VideoPreProcessor():
    def __init__(self):
        super().__init__()

    def convert_video_format(self, video, from_format, to_format, fps):
        # TODO: AVI conversion here
        # Use something similar to: ffmpeg -loglevel error -y -i ./test_video.avi -crf 0 -pix_fmt yuv420p ./test_video2.avi
        pass
    
    def process_video(self, video, metadata):
        if metadata['format'] != 'avi':
            self.convert_video_format(video, metadata['format'], 'avi')
                
        frames = video.split(bytes.fromhex('30306463'))
        iframe = bytes.fromhex('0001B0')
        pframe = bytes.fromhex('0001B6')
        blankframe = bytes.fromhex('')
        
        
        iframe_indices = []
        pframe_indices = []

        for (index, frame) in enumerate(frames):
            if frame[5:8] == iframe:
                iframe_indices.append(index)
            elif frame[5:8] == pframe:
                pframe_indices.append(index)
        
        if pframe_indices[-1] > iframe_indices[-1]:
            iframe_indices.append(pframe_indices[-1]+1)
        
        header = frames[:iframe_indices[0]]
        
        video_obj = VideoObject()

        start = None
        for end_index in iframe_indices:
            if start == None:
                start = end_index
            else:
                content = frames[start:end_index]
                full_content = header + content
                dataout = bytes.fromhex('30306463').join(full_content) #+ bytes.fromhex('30306463')
                video_obj.add_chunk(VideoChunkObject(dataout, len(header)))
                start = end_index

        return video_obj



        
    
