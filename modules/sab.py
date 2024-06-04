# MAIN execution file for semiautomaticbrainrot process
# inputs: reddit url containing a comment
# outputs: a tiktok video with automatic subtitles and tts speech, with minecraft parkour footage in the background

from moviepy import *
from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip
from maketts import commentTTS
import random, json
import assemblyai as aai
import asyncio

bg_videos_list = os.path.join(os.path.dirname(__file__), '../bg_videos/videos.json')
bg_videos_dir = os.path.join(os.path.dirname(__file__), '../bg_videos/')
output_path = os.path.join(os.path.dirname(__file__), '../output/output.mp4')
logs_path = os.path.join(os.path.dirname(__file__), '../logs/')

# main function
async def makeBaseVideo(url):

    # get TTS speech file and create movie audio
    # using the default voice id for Nassim
    tts_path = await commentTTS(url, "repzAAjoKlgcT2oOAIWt")
    audio = AudioFileClip(tts_path)
    audio_duration = audio.duration
    print("Sucessfully created new audio clip of " + str(audio_duration) + "...")

    # get random background clip as variable bg, assuming 1920x1080p resolution
    (timecode, name) = getRandomVideo(audio_duration)
    bg = VideoFileClip(bg_videos_dir+name).subclip(timecode, int(timecode+audio_duration))
    print("Sucessfully created new video clip of " + str(bg.duration) + "...")

    # crop bg footage to be vertical video 1080x608 or otherwise 9:16 sized video
    # for some reason the video ends up being square? not sure why.
    (w, h) = bg.size
    bg_crop = crop(bg, width=int(w*(9/16)), height=h, x_center=w/2, y_center=h/2)
    bg_crop.audio = audio
    print("Added audio layer...", end="\t")

    # add the subtitles according to the audio
    subtitles = getSubtitlesFromAudio(tts_path)
    composite_result = CompositeVideoClip([bg_crop, subtitles.set_pos(('center'))])
    print("Added subtitles layer", end="\t")
    
    # write the composited video file
    composite_result.write_videofile(output_path, fps=bg_crop.fps)
    print("Generated full video sequence", end="\t")
    
    return 


# picks a random video from the bg_videos folder and selects a random time period
def getRandomVideo(audio_duration):

    # open clips dictionary
    with open(bg_videos_list) as data:
        videos = json.load(data)
        print("Type: ", type(videos))
        video = random.choice(list(videos.items()))
        name = video[0]
        time = int(video[1])

    print("selected random video ", name, " with length ", time)

    # select a random time period
    time_start = random.randint(60, time - 60 - int(audio_duration))
    print("selected random time period from ", time_start, " to ", time_start + int(audio_duration))
    return time_start, name

aai.settings.api_key = "8b3d3a5e057e4094a3022f113b8636fb"

# create subtitles from the audio
def getSubtitlesFromAudio(audio_path):
    FILE_URL = audio_path
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)
    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
    else:
        print(transcript.text)
    srt = transcript.export_subtitles_srt(chars_per_caption=32)
    s = open(logs_path+"/subtitles.srt", "w")
    s.write(srt)
    s.close()
    
    generator = lambda txt: TextClip(txt, font="Simply-Rounded-Bold", fontsize=32, color='white')
    subs = SubtitlesClip(logs_path+"subtitles.srt", generator)
    subtitles = SubtitlesClip(subs, generator)

    return subtitles

# example called when using python modules/sab.py
if __name__ == "__main__":
    print("Creating new video from URL: https://www.reddit.com/r/AskReddit/comments/oeo0h/comment/c3gs5gp/")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(makeBaseVideo("https://www.reddit.com/r/AskReddit/comments/oeo0h/comment/c3gs5gp/"))
    print("Completed")
    exit()

# TODO
# !! SUBTITLES ARE PERFECT !!
# DEFINE SUBTITLE FORMAT AS MORE APPEALING STYLE (done in txttest.py, just need to implement here)
# GENERATE PNG OF POST TITLE