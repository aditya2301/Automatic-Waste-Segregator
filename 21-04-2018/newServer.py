from tensorFlow import identification
import socket,sys,os            
import datetime


def extractForegroundImage(img_name):
    img_rgb = cv2.imread(os.path.join("static",directory,img_name))

    img = cv2.cvtColor(img_rgb,cv2.COLOR_RGB2HSV)
    img = cv2.bilateralFilter(img,9,105,105)

    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    ret,thresh_image = cv2.threshold(gray,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    equalize= cv2.equalizeHist(thresh_image)


    canny_image = cv2.Canny(equalize,250,255)
    canny_image = cv2.convertScaleAbs(canny_image)
    kernel = np.ones((3,3), np.uint8)
    dilated_image = cv2.dilate(canny_image,kernel,iterations=1)

    new,contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    c=contours[0]
    final = cv2.drawContours(img, [c], -1, (255,0, 0), 3)

    mask = np.zeros(img_rgb.shape[:2],np.uint8)
    new_image = cv2.drawContours(mask,[c],0,255,-1,)
    new_image = cv2.bitwise_and(img_rgb,img_rgb,mask=mask)

    cv2.imwrite(os.path.join("static",directory,img_name),new_image)


s = socket.socket()         
port = 60000
host = socket.gethostname()
print(host)               
print(os.getcwd())
s.bind((host, port))        
s.listen(5)     
print("Socket is listening")            
while True:
   try:
      c, addr = s.accept()     
      print('Got connection from', addr)
      length=c.recv(10)
      length=int(length.decode("utf-8"))
      c.send(bytes('OK','utf-8'))
      name='Image-'+datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")+'.jpeg'
      
      directory=datetime.datetime.now().strftime("%d-%m-%y")
      if not os.path.exists(os.path.join(os.getcwd(),directory)):
         os.makedirs(directory)

      with open(os.path.join("static",directory,name),"wb") as f:
         for i in range(0,length):
            data=c.recv(1)
            f.write(data)

      #extractForegroundImage(directory,name)
      value=identification(os.path.join("static",directory,name))
      c.send(bytes(value,"utf-8"))
      c.close()

   except KeyboardInterrupt:
      c.close()
      s.close()
      break
      
   except Exception as e:
    if type(e).__name__=="EOFError":
      sys.exit()
   	print(e)
   	c.close()
   	continue

