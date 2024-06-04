import json
from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=NX-i0IWl3yg')
yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path="../bg_videos/")
length_seconds = yt.length

with open('../bg_videos/videos.json', 'w') as data:
        vids = json.load(data)
        vids[yt.title] = length_seconds
        json.dump(vids, data, indent=4)

print("Successfully downloaded video stream")