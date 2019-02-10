import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def get_img_text(file_name):
	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	# The name of the image file to annotate
	file_name = os.path.join(
	    os.path.dirname(__file__),
	    file_name)

	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
	    content = image_file.read()

	image = vision.types.Image(content=content)

	response = client.text_detection(image=image)

	texts = response.text_annotations

	transcription = ' '.join([text.description for text in texts])
	return transcription
print(get_img_text('notes.jpg'))