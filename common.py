from flask import Flask, url_for, redirect, render_template, request, Blueprint
import time
import json
import requests
#import db
import sys
import db
import nltk
import os
import re
import io
from werkzeug import secure_filename
import importlib
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
importlib.reload(sys)

from rake_nltk import Rake

r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.
# sys.setdefaultencoding('utf-8')
# model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)


commonPages = Blueprint('commonPages', __name__)


#-----------------Routing--------------------------------
@commonPages.route("/", methods = ['POST', 'GET'])
def index():
    return redirect(url_for('commonPages.main'))

@commonPages.route("/main", methods = ['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template("main.html")
    if request.method == 'POST':
        searchcontent = request.form["search"]
        return redirect(url_for('commonPages.displayresults', question = searchcontent))

@commonPages.route('/upload')
def upload_file():
    return render_template('my-form.html')

@commonPages.route('/uploader', methods = ['GET', 'POST'])
def upload_file_post():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        client = speech.SpeechClient()
        print(secure_filename(f.filename))
        with io.open(secure_filename(f.filename), 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,sample_rate_hertz=44100,language_code='en-US')
        response = client.recognize(config, audio)
        text = ""
        for result in response.results:
            text += result.alternatives[0].transcript
            print(result.alternatives[0].transcript)
        with open("text.txt", "w") as f:
            f.write(text)
        r.extract_keywords_from_text(text)
        return render_template("displayresults.html", keynote = r.get_ranked_phrases()[0:6], source = text)

@commonPages.route("/displayresults", methods = ['POST', 'GET'])
def displayresults():
    question = request.args.get('question')
    if request.method == 'GET':
        if valid_or_not(question):
            r.extract_keywords_from_text(question)

            temp, mainwords, judgement = ["abc", ["sadasd","asdas"],["adsa"]], "csa", "adsa"
#            db.writequestion(question, mainwords)
            return render_template("displayresults.html", keynote = r.get_ranked_phrases()[0:6])
        else:
            return redirect(url_for('commonPages.notfound'))
    if request.method == 'POST':
        searchcontent = request.form["search"]
        return redirect(url_for('commonPages.displayresults', question = searchcontent))

@commonPages.route("/notfound", methods = ['POST', 'GET'])
def notfound():
    if request.method == 'GET':
        return render_template("notfound.html")
    if request.method == 'POST':
        searchcontent = request.form["search"]
        return redirect(url_for('commonPages.displayresults', question = searchcontent))

def search_for_result(sentence):
    return ["abc","c"], "bcs", "adsada"

def valid_or_not(searchcontent):
    return True

def process_content():
    try:
        result = []
        for i in tokenized[:5]:
            words = nltk.word_tokenize(i)
            return  nltk.pos_tag(words)
            # print(tagged)
        return result

    except Exception as e:
        print("error: "+str(e))
