import os
import speech_recognition as sr
from tqdm import tqdm
from multiprocessing.dummy import Pool

def get_transcript(file_name, key_name):
    NUM_THREADS = 100 # Number of concurrent threads
    r = sr.Recognizer()
    with open(key_name) as f:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

    def transcribe(data):
        idx, file = data
        name = "parts/" + file
        print(name + " started")
        # Load audio file
        with sr.AudioFile(name) as source:
            audio = r.record(source)
        # Transcribe audio file
        text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print(name + " done")
        return {
            "idx": idx,
            "text": text
        }

    pool = Pool(NUM_THREADS)
    os.system("mkdir parts")
    os.system("ulimit -n 2048")
    command = 'ffmpeg -i "{}" -f segment -segment_time 28 -c copy parts/out%09d.wav'.format(file_name)
    os.system(command)
    files = sorted(os.listdir('parts/'))
    all_text = pool.map(transcribe, enumerate(files))
    pool.close()
    pool.join()

    transcript = ""
    for t in sorted(all_text, key=lambda x: x['idx']):
        # Format time as h:m:s - 30 seconds of text
        transcript += "{}\n".format(t['text'])
    os.system("rm -rf parts")
    return transcript

#print(get_transcript('MS&E 472 (long).wav', "api-key.json"))