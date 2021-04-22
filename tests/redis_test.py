from videovault import VideoVault

def test_video_storage():
    vdb = VideoVault({'storage': 'redis'})
    with open("./friends2.mp4", 'rb') as videofile:
        video = videofile.read()
        res = vdb.store_video("02", video)
        
        # assert res == "02"
        # response = vdb.get_video("01")
        # print(response)
        # response = vdb.get_video_frame("01", 26)
        # print(vdb.get_every_nth_video_frame("01", 10))
        # assert response['metadata'] == metadata
        # assert response['video'] == video
        # print(response['video'].get_num_frames())


if __name__ == "__main__":
    test_video_storage()
    print("Tests Passed")