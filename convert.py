from pydub import AudioSegment
song = AudioSegment.from_mp3("Stephanie Sucks.mp3")
song.export("out.linear16", format="linear16")
