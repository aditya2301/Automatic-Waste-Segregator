from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='df0093d074f8489c88cc8bb7894b94c9')

model = app.models.get("general-v1.3")
model = app.models.get('general-v1.3')
image = ClImage(file_obj=open('/home/pi/Desktop/DetectedObjects.jpg', 'rb'))
#print(model.predict([image]))

#labels={model.predict([image])['outputs'][2]}
l=model.predict([image])['outputs'][0]['data']['concepts']
                
for i in l:
	print(i['name'])
