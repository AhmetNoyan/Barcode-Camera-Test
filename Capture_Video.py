import cv2 as cv
import time
  

start1 = time.time()
cap = cv.VideoCapture(0,cv.CAP_DSHOW)  
print("Video Capture Started")
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640) #Set Frame width
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480) #Set Frame hight
print("FPS: "+str(cap.get(cv.CAP_PROP_FPS)))
print("width " +str(cap.get(cv.CAP_PROP_FRAME_WIDTH))+"\n"+"Height "+str(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
cap.set(cv.CAP_PROP_AUTOFOCUS,0)#Autofocus OFF 
focus=100
cap.set(cv.CAP_PROP_FOCUS,focus)
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)#Auto exposure off
expo=-6
cap.set(cv.CAP_PROP_EXPOSURE, expo)
end1 = time.time()
print("time to turn it on "+str("%.2f"%(end1-start1))+" seconds")

  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = cap.read()
  
    # Display the resulting frame
    cv.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv.destroyAllWindows()