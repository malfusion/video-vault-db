from .video import VideoObject
from .videochunk import VideoChunkObject
from subprocess import Popen, PIPE
import json

class VideoPreProcessor():
    def __init__(self):
        super().__init__()

    def standardize_video_format(self, video, from_format, to_format, fps):
        # TODO: AVI conversion here
        # Use something similar to: 
        cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-i', 'pipe:0', '-crf', '0', '-pix_fmt', 'yuv420p', 'pipe:1']
        p = Popen(cmd, stdin=PIPE, stdout=PIPE)
        output_video = p.communicate(input=video)[0]
        return output_video
        

    def get_video_metadata(self, video):
        cmd = ['ffprobe', '-loglevel', 'panic','-select_streams', 'v:0', '-show_streams', '-print_format', 'json', 'pipe:0']
        p = Popen(cmd, stdin=PIPE, stdout=PIPE)
        output = p.communicate(input=video)[0]
        props = json.loads(output)
        return props['streams'][0]
    
    def process_video(self, video):
        metadata = self.get_video_metadata(video)
                
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



        
    
