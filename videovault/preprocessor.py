

class VideoPreProcessor():
    def __init__(self):
        super().__init__()

    def convert_video_format(self, video, from_format, to_format, fps):
        # TODO: AVI conversion here
        # Use something similar to: ffmpeg -loglevel error -y -i ./test_video.avi -crf 0 -pix_fmt yuv420p -r 30 ./test_video2.avi
        pass
    
    def process_video(self, video, metadata):
        if metadata['format'] != 'avi':
            self.convert_video_format(video, metadata['format'], 'avi')
                
        frames = video.split(bytes.fromhex('30306463'))
        iframe = bytes.fromhex('0001B0')
        pframe = bytes.fromhex('0001B6')
        blankframe = bytes.fromhex('')
        
        print("Total frames", len(frames))
        
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

        start = None
        for end_index in iframe_indices:
            if start == None:
                start = end_index
            else:
                content = frames[start:end_index]
                full_content = header + content
                dataout = bytes.fromhex('30306463').join(full_content) + bytes.fromhex('30306463')
                out_file = open("./outputtest_" + str(start) + "_" + str(end_index) + ".avi", 'wb')
                out_file.write(dataout)
                out_file.close()
                start = end_index



        # print(iframe_indices)


        # iframes_cnt = 0
        # pframes_cnt = 0
        # blankframes_cnt = 0
        
        # out_file = open("./outputtest.avi", 'wb')
        
        # start = False
        # end = False
        
        # for index, frame in enumerate(frames):
            
        #     if frame[5:8] == iframe:
        #         iframes_cnt += 1
        #         print("III", index, len(frame))
        #         if not start and not end:
        #             start = True
        #         elif start and not end:
        #             end = True

        #     elif frame[5:8] == pframe:
        #         pframes_cnt += 1
        #         print("P", index, len(frame))
        #     elif frame[5:8] == blankframe:
        #         blankframes_cnt += 1
        #         print("Blank", index, len(frame))
        #     else:
        #         if not end:
        #             print("Writingb", index)
        #             out_file.write(frame + bytes.fromhex('30306463'))
        #         print("???????", len(frame))

        #     if start and not end:
        #         print("Writingc", index)
        #         out_file.write(frame + bytes.fromhex('30306463'))

            
        


            # print(frame[5:8], len(frame), frame[:8] == pframe)

            # if  i_frame_yet == False or index < int(start_effect_sec * fps) or index > int(end_effect_sec * fps):
            #     # the split above removed the end of frame signal so we put it back in
            #     out_file.write(frame + bytes.fromhex('30306463'))

            #     # found an i-frame, let the glitching begin
            #     if frame[5:8] == iframe: i_frame_yet = True

            # else:
            #     # while we're moshing we're repeating p-frames and multiplying i-frames
            #     if frame[5:8] != iframe:
            #         # this repeats the p-frame x times
            #         for i in range(repeat_p_frames):
            #             out_file.write(frame + bytes.fromhex('30306463'))

                

        # print("I-frames:", iframes_cnt)
        # print("P-frames:", pframes_cnt)
        # print("Blank frames:", blankframes_cnt)
        # out_file.close()
            



        
    
