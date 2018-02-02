from time import sleep
from picamera import PiCamera
import dropbox,os,datetime



image_name="File-"+datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")+".jpg"
camera = PiCamera()
camera.resolution = (512, 512)
print("Capturing the image. . ..")
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture(image_name)
print("This is the image captured . . .")
os.system("xdg-open "+image_name)
dbx=dropbox.Dropbox('API KEY')
print("Uploading the file to dropbox . . ")

with open(image_name,"rb")as f:
	file=f.read()
dbx.files_upload(file, "/imageFiles/"+image_name, mode=dropbox.files.WriteMode.overwrite)
print("Successful !")

while True:
    sleep(30)
    
    dbx.files_download_to_file("//home/pi//Desktop//imageClassifierResult.txt","/imageFiles/imageClassifierResult.txt",rev=None)

    with open("imageClassifierResult.txt","r")as f:
        data=f.readlines()

    if data[-1]=="\n":
        data=data[-2]
    else:
        data=data[-1]
    data=data.split()
    category=data[1]
    ratio=data[2]
    data=data[0]
    
    if data==image_name:
        break


print("Identified as -")
print("Category-",category)
print("Ratio-",ratio)
