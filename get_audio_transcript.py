import os
import speech_recognition as sr
from tqdm import tqdm
from multiprocessing.dummy import Pool

def getExtension(path):
        """
        Gets the file extension from path

        :param str path: Path of the file

        :returns: File extension
        :rtype: str
        """
        filename, file_extension = os.path.splitext(path)
        return file_extension

def get_audio_transcript(file_name, key_name):
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
    targDir = "parts"
    os.system("mkdir {}".format(targDir))
    os.system("ulimit -n 2048")
    ext = getExtension(file_name)
    if ext == '.mp4':
        os.system('ffmpeg -i "{}" -acodec pcm_s16le -ac 1 -ar 8000 "{}".wav'.format(file_name, file_name))
        command = 'ffmpeg -i "{}.wav" -f segment -segment_time 27 -c copy {}/out%09d.wav'.format(file_name, targDir)
        os.system(command)
        os.system('rm -rf "{}.wav"'.format(file_name))
    elif ext == '.wav':
        command = 'ffmpeg -i "{}" -f segment -segment_time 27 -c copy {}/out%09d.wav'.format(file_name, targDir)
        os.system(command)
    files = sorted(os.listdir('{}/'.format(targDir)))
    all_text = pool.map(transcribe, enumerate(files))
    pool.close()
    pool.join()

    transcript = ""
    for t in sorted(all_text, key=lambda x: x['idx']):
        transcript += "{}\n".format(t['text'])
    os.system("rm -rf {}".format(targDir))
    return transcript

#print(get_transcript('MS&E 472.mp4', "api-key.json"))