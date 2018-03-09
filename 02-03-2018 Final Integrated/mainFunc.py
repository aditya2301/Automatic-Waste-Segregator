from label_image import identification
import time

start=time.time()
value=identification("5.jpeg")
print(time.time()-start)
print(value)

