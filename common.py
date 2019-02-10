from flask import Flask, url_for, redirect, render_template, request, Blueprint
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from get_audio_transcript import get_audio_transcript
from get_summary import get_summary
from get_img_text import get_img_text
from werkzeug import secure_filename
from twilio.rest import Client
from send_message import send_message
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
import importlib
importlib.reload(sys)

from rake_nltk import Rake

totalSize = 0
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
        return render_template("displayresults.html")
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
        ext = getExtension(f.filename)
        text = ""
        if ext == '.mp4' or ext == '.wav':
            text = get_audio_transcript(secure_filename(f.filename))
        else:
            text = get_img_text(secure_filename(f.filename))
        print(text)
        send_message(f.filename, file_size(secure_filename(f.filename)), convert_bytes(totalSize))
        return render_template("displayresults.html", summary_sentences = get_summary(text), source = text)

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

def getExtension(path):
        """
        Gets the file extension from path

        :param str path: Path of the file

        :returns: File extension
        :rtype: str
        """
        filename, file_extension = os.path.splitext(path)
        return file_extension

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        global totalSize
        totalSize = totalSize + file_info.st_size
        return convert_bytes(file_info.st_size)
