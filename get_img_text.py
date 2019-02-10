import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def get_img_text(file_name):
	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
	    content = image_file.read()

	image = vision.types.Image(content=content)

	response = client.text_detection(image=image)

	texts = response.text_annotations

	return texts[0].description
#print(get_img_text('notes.jpg'))