import redditscraper as r
import os
import requests

# get audio path and set chunk size
audio_path = os.path.join(os.path.dirname(__file__), '../logs/tts_log.mp3')
CHUNK_SIZE = 1024

# dictionary of voice names and corresponding ID's from ElevenLabs
voices = {
    "Nassim" : "repzAAjoKlgcT2oOAIWt"
}
1
# my api key
api_key = "8417d9fa5b93528fb7e930088ddb1bbc"

# create the script from the comment using redditscraper
def makeScript(comment):
    body = comment.getCommentBody()
    post = comment.post
    print(str(f"{post},...,{body}"))
    return str(f"{post},...,{body}")

# create the AI voiceover from the script
def makeTTS(script, voice):

    # it's important to detect any issues before paying for them, and I think in the future it'll be useful to manually check output before creating a VO
    if not os.path.isfile(audio_path):
        raise Exception(f"Failed to find audio path at {audio_path}")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": script,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    # pretty simple, get the response binary, split it into chunks, write to an mp3 file
    response = requests.post(url, json=data, headers=headers)
    with open(audio_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    
    print("Generated tts audio succesfully...")

def commentTTS(url, voice):
    comment = r.RedditComment(url)
    # create tts file with script
    makeTTS(makeScript(comment), voice)
    return audio_path

def _debug(url):
    commentTTS(url, voices["Nassim"])


# _debug("https://www.reddit.com/r/AskReddit/comments/1bg7hud/comment/kv5p5us/")