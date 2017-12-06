import io
from google.cloud import vision

vision_client = vision.Client()
file_name = '260px-Russia_v_Argentina_-_Lionel_Messi.jpg'

with io.open(file_name,'rb')as i_f:
    content=i_f.read()
    image=vision_client.image(content=content)


labels=image.detect_labels()

for label in labels:
    print(label.description)


