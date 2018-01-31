




from google.cloud import vision
from google.cloud.vision import types
import io,os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'VisionTest-7f235331762e.json'


# Instantiates a client
client = vision.ImageAnnotatorClient()


print("Reading the Image file. . .")
with io.open("img.jpg", 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

print("Receiving response from Google API. . .")
response = client.document_text_detection(image=image)
labels = response.full_text_annotation



from gtts import gTTS
import os    
print("Converting your text to sound . . .")
tts = gTTS(text=labels.text, lang='en')
tts.save("pcvoice.mp3")
print("Starting audio. . .")
os.system("start pcvoice.mp3")
print("Thank You !!")
