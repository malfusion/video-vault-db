from .video import VideoObject
from .videochunk import VideoChunkObject
from subprocess import Popen, PIPE
import json
import tempfile
import os 

class VideoProcessor():
    def __init__(self):
        super().__init__()


    def standardize_video_format(self, video, input_format):
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(video)
            cmd = ['ffmpeg', '-i', os.path.realpath(tmp.name), '-crf', '0', '-qscale', '0', '-pix_fmt', 'yuv420p',  '-r', '25', '-f', 'avi', 'pipe:1']
            p = Popen(cmd, stdout=PIPE)
            output_video = p.stdout.read()
            return output_video
        return None

    def get_frame_from_video(self, video, frame_num):
        cmd = ['ffmpeg', '-loglevel', 'error', '-i', 'pipe:0', '-f', 'singlejpeg', '-vf', 'select=eq(n\,'+str(frame_num)+')', 'pipe:1']
        p = Popen(cmd, stdin=PIPE, stdout=PIPE)
        output_img, stderr = p.communicate(input=video)
        return output_img
        

    def get_video_metadata(self, video):
        cmd = ['ffprobe', '-loglevel', 'panic','-select_streams', 'v:0', '-show_streams', '-print_format', 'json', 'pipe:0']
        p = Popen(cmd, stdin=PIPE, stdout=PIPE)
        output, stderr = p.communicate(input=video) 
        props = json.loads(output)
        if stderr:
            print(stderr)
        return props['streams'][0]


    def split_chunks_video(self, video):
        frames = video.split(bytes.fromhex('30306463'))
        iframe = bytes.fromhex('0001B0')
        pframe = bytes.fromhex('0001B6')
        blankframe = bytes.fromhex('')
        print("Frames:", len(frames))
        iframe_indices = []
        pframe_indices = []

        for (index, frame) in enumerate(frames):
            if frame[5:8] == iframe:
                iframe_indices.append(index)
            elif frame[5:8] == pframe:
                pframe_indices.append(index)
        
        if pframe_indices and iframe_indices:
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
                video_obj.add_chunk(VideoChunkObject(dataout, start, len(header)))
                start = end_index
        return video_obj



        
    
