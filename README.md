# NoteDex

## Inspiration
The Student Disability Center on campus often requests note takers to assist students with disabilities, but often, these positions go unfilled. This is detrimental to student with learning disabilities such as deafness or attention-deficit. We saw this as an opportunity to apply natural language processing, text sentiment analysis, OCR, and state of the art speech-to-text software to help these students. In addition,

## What it does
NoteDex can take in three types of input - audio, video, and images (handwritten or typed). It outputs a comprehensive text based on the input as well as a summary of the content.

## How we built it
We leveraged Google cloud services, notably Google speech-to-text and OCR, to process our input data. To optimize for large audio/video files, we implemented multithreading in python to speed up the time from 55 minutes to under 30 seconds. To interface these features, we used the Flask framework along with HTML templates. Finally, we deployed using Google's Compute Engine. Afterwards, we ran a customized TextRank summarization algorithm on that outputted text using natural language processing principles, where we selected the most important sentences based on a combination of TextRank weights and Rapid Automatic Keyword Extraction (RAKE) outputs. Finally, we included Twilio to text ourselves analytics regarding file size and submission to monitor usage and pricing information.

## Challenges we ran into
One major obstacle we ran into with Google speech-to-text was with the maximum length of video and audio features we could process. We were only allowed to process one minute at a time using synchronous recognition and asynchronous recognition required us to upload already large files to the cloud, reducing efficiency. We solved this by splitting the file into 100 threads, which all ran independently, vastly decreasing run-time.

Additionally, natural language summarization was a much more difficult problem than we had thought, and we realized that we probably could not obtain enough data to run a specific deep learning algorithm. We tried two summarization models - one using GloVe (Global Vectors for Word Representation) and the others using a custom RAKE/bag-of-words representation, which we ended up using for efficiency reasons.

Finally, deployment was also a major challenge. We didn't have much experience with deployment, and we started from the ground up. It was a substantial challenge to handle billing issues and installing packages on a different environment.

Also, half of the team members were new to using Github, and code management was a challenge at times.

## Accomplishments that we're proud of
This was the first substantial hackathon for half of the team, and it was awesome to actually create a running product. We had just learning multithreading a week ago in a computer science class through a more theoretical lens, and it was exciting to use it in a real world application. Finally, it was cool to learn to use APIs like Twilio's and Google's cloud computing services!

Full post here: https://devpost.com/software/notedex

INSTALLATION (DEVELOPERS)
------------
*Use python3 and pip3 for installation of the packages.*

> export GOOGLE_APPLICATION_CREDENTIALS=api-key.json

> python3 ir_main.py

The application will run on http://0.0.0.0:80/ or http://localhost 





