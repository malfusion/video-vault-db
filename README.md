# VideoVault
A video storage and retrieval engine with support for frame-level video queries.
The primary aim is to abstract away the many pains of dealing with video, including image thumbnail extraction, trimmed video retrieval, periodic image retrieval, etc

## Applications

-  Time-series analysis of videos
-  Deep learning applications
-  Thumbnail generation
-  Dataset creation

## Usage:
- Ensure Redis is running at the default port under localhost.

- Initialize a VideoVault DB object.

  ```python 
  vdb = VideoVault({'storage': 'redis'})
  ```
- Store a video file along with a unique ID, the file is broken down, indexed and stored in Redis.
  ```python
    with open("./friends.mp4", 'rb') as videofile:
      data = videofile.read()
      response = vdb.store_video("friends_clip_01", data)
  ```
- You can retrieve a single frame from a video by its frame number:
  ```python
    frame = vdb.get_video_frame("friends_clip_01", 1800)
  ```
- You can retrieve a every-nth-frame (here every 100th frame) from a video:
  ```python
    frames = vdb.get_every_nth_video_frame("friends_clip_01", 100)
  ```
