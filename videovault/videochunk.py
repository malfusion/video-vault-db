class VideoChunkObject():
    def __init__(self, chunkBytes, contentStartFrame):
        super().__init__()
        self.bytes = chunkBytes
        self.contentStartFrame = contentStartFrame

    def get_bytes(self):
        return self.bytes
    
    def get_num_frames(self):
        return len(self.bytes.split(bytes.fromhex('30306463'))) - self.contentStartFrame
    
    