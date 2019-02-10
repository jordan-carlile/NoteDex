import bs4 as bs  
import urllib.request
import re
import nltk
import heapq
import numpy as np 
import pandas as pd
from nltk.tokenize import sent_tokenize
from rake_nltk import Rake

def open_file(file_name):
	with open(file_name, 'r') as file:
		article_text = file.read()
	article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
	article_text = re.sub(r'\s+', ' ', article_text)

	return article_text

def summary_sent(file_name, num, article_text):


	formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
	formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  
	sentence_list = nltk.sent_tokenize(article_text)

	stopwords = nltk.corpus.stopwords.words('english')

	word_frequencies = {}  
	for word in nltk.word_tokenize(formatted_article_text):  
	    if word not in stopwords:
	        if word not in word_frequencies.keys():
	            word_frequencies[word] = 1
	        else:
	            word_frequencies[word] += 1

	maximum_frequncy = max(word_frequencies.values())

	for word in word_frequencies.keys():  
	    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

	sentence_scores = {}

	for sent in sentence_list:  
	    for word in nltk.word_tokenize(sent.lower()):
	        if word in word_frequencies.keys():
	        	if len(sent.split(' ')) < 30:
		        	if sent not in sentence_scores.keys():
		        		sentence_scores[sent] = word_frequencies[word]
		        	else:
		        		sentence_scores[sent] += word_frequencies[word]
		        else:
		        	if sent not in sentence_scores.keys():
		        		sentence_scores[sent] = 0


	summary_sentences = sorted(sentence_scores.items(), key=lambda kv: -kv[1])
	summary_sentences = [s[0] for s in summary_sentences]

	# summary_sentences = heapq.nlargest(10, sentence_scores, key=sentence_scores.get)

	summary = ' '.join(summary_sentences[:num])  
	return [summary, summary_sentences]

def topic_extraction(summary_sentences, k, content, topics):
	r = Rake()

	r.extract_keywords_from_text(content)
	top_phrases = r.get_ranked_phrases()[:10]
	print("TOP PHRASES", top_phrases)
	for phrase in top_phrases:
		phrase = re.sub('[^a-zA-Z0-9]', ' ', phrase).strip()
		phrase = re.sub(r'\s+', ' ', phrase)
		for sent in summary_sentences:
			stripped = re.sub('[^a-zA-Z0-9]', ' ', sent).strip()
			stripped = re.sub(r'\s+', ' ', stripped)
			# print("TEXT ", sent)
			# print("stripped", stripped)
			if phrase in stripped.lower():
				topics.append(sent)


def main():
	file_name = "ai.txt"

	content = open_file(file_name)
	num = 15
	# summary_sentences = []
	smry, summary_sentences = summary_sent(file_name, num, content)
	print("summary ", smry)


	# print(summary_sentences)
	smry_file = open(file_name.split('.')[0] + "_summary.txt", "w")
	smry_file.write(smry)
	smry_file.close()

	k = 10
	topics = []
	topic_extraction(summary_sentences, 10, content, topics)
	print(topics) # topics related to the rake return

if __name__ == '__main__':
	main()

