class VideoChunkObject():
    def __init__(self, chunkBytes, start_frame_in_full_video, content_offset):
        super().__init__()
        self.bytes = chunkBytes
        self.content_offset = content_offset
        self.start_frame_in_full_video = start_frame_in_full_video

    def get_bytes(self):
        return self.bytes
    
    def get_start_frame(self):
        return self.start_frame_in_full_video
    
    def get_content_offset(self):
        return self.get_content_offset
    
    def get_num_frames(self):
        return len(self.bytes.split(bytes.fromhex('30306463'))) - self.content_offset
    
    