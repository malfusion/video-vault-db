from videovault import VideoVault

def test_video_storage():
    vdb = VideoVault({'storage': 'memory'})
    with open("./test_video.avi", 'rb') as videofile:
        video = videofile.read()
        res = vdb.store_video("01", video)
        assert res == "01"
        response = vdb.get_video("01")
        # assert response['metadata'] == metadata
        # assert response['video'] == video
        print(response['video'].get_num_frames())


if __name__ == "__main__":
    test_video_storage()
    print("Tests Passed")