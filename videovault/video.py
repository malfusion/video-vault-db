class VideoObject():
    def __init__(self, chunks=[]):
        super().__init__()
        self.chunks = chunks
    
    def add_chunk(self, chunk):
        self.chunks.append(chunk)
    
    def get_chunks(self):
        return self.chunks

    def get_num_frames(self):
        print([chunk.get_num_frames() for chunk in self.chunks])
        return sum([chunk.get_num_frames() for chunk in self.chunks])