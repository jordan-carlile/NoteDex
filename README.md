# keynoteextractor

INTRODUCTION
------------

KeyPoints aims to address this issue by providing an individualized alternative learning method for students. By simply recording a lecture, students can then upload the audio file to keynote and the web app will summarize and compile a list of main idea notes from the lecture. Using Google Cloud Speech API to transcribe the lecture and RAKE keyword identifier technology, the web app returns a list of key ideas or arguments from the audio recording.

We have included a file called China.wav that you can try.

INSTALLATION
------------
*Use python3 and pip3 for installation of the packages.*

> export GOOGLE_APPLICATION_CREDENTIALS=api-key.json

> python3 ir_main.py

The application is running on http://0.0.0.0:8080/

TROUBLESHOOTING
---------------

The audio file must be mono channel .wav file in order for it to work.



