import numpy as np
import cv2 as cv
import time
import pylibdmtx #Library for barcode reading
from pylibdmtx import pylibdmtx
from PIL import Image
import glob


barcodes=[]
font = cv.FONT_HERSHEY_SIMPLEX
crop_state=False
global expo
global focus
global cap
global width
global height
global r
global C1
r=[]

 


def main():

    while(True):
        print("RESOLUTION OPTIONS\n1)640x480\n2)800x600\n3)1280x720\n4)1600x1200\n5)1920x1080\n6)2048x1536\n7)2592x1944")
        num=input("Please select resolution(type 1,2,3,4,5,6 or 7)")
        if(int(num)==1):
            width=640
            height=480
            r=[1,101,639,134]#Default barcode area
            break
        elif(int(num)==2):
            width=800
            height=600
            r=[1,131, 799,171]#Default barcode area
            break
        elif(int(num)==3):
            width=1280
            height=960
            r=[1,208,1279,289]#Default barcode area
            break
        elif(int(num)==4):
            width=1600
            height=1200
            r=[1,208,1279,289]#Default barcode area
            break
        elif(int(num)==5):
            width=1920
            height=1080
            r=[1,211,1919,363]#Default barcode area
            break
        elif(int(num)==6):
            width=2048
            height=1536
            r=[75,516,1973,261]#Default barcode area
            break
        elif(int(num)==7):
            width=2592
            height=1944
            r=[81,518,1967,272]#Default barcode area
            break
        else:
            print("try again")
        

    print("Selected resolution: "+str(width)+"x"+str(height))
    start1 = time.time()
    cap = cv.VideoCapture(0)  
    print("Video Capture Starts")
    expo = cap.get(cv.CAP_PROP_EXPOSURE)  
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width) #Frame width
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height) #Frame hight
    print("FPS: "+str(cap.get(cv.CAP_PROP_FPS)))
    print("width " +str(cap.get(cv.CAP_PROP_FRAME_WIDTH))+"\n"+"Height "+str(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
    cap.set(cv.CAP_PROP_AUTOFOCUS,0)#Autofocus OFF 
    ret, frame = cap.read() #get the frame from camera
    focus=95#set to 8 cm distance focus
    cap.set(cv.CAP_PROP_FOCUS,focus)
    print("focused to ROI")
    cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
    print("Auto exposure off")
    expo=-6#15.6 ms
    cap.set(cv.CAP_PROP_EXPOSURE, expo)
    print("Exposure set to 4 ms")
    C1=0
        
    print("Keyboard Control Keys:\nw : increases focus value\ns : decreases focus parameter\na : autofocus ON")
    print("t : reads barcodes from the frame and save it to the path(make sure to change the path\nb : decreases exposure time")
    print("m : increases exposure time\nn : auto exposure OFF\nc : auto exposure ON\nf : focus 8 cm\nr : Select ROI for Barcode\ny : Select ROI for Plate Absence-Presence\nq : EXIT")
    end1 = time.time()
    print("time to turn it on "+str(end1-start1)+" seconds")
    while True:
        
        ret, frame = cap.read() 
        frame = cv.rotate(frame, cv.ROTATE_180)
        if not ret:
            print("Can't receive frame.Please check your camera connection")
            break
        
        cv.imshow('Video', frame)
        k=cv.waitKey(1) #get the pressed key
    
        if k == ord('w') :# if key is "w", increase the focus parameter
            focus=focus+5
            if focus>=720:
                focus=720
            cap.set(cv.CAP_PROP_FOCUS,focus)#set focus
            print ("focus: "+str(focus))#Print the focus parameter
            
        
        elif k == ord('s'):# if key is "s", decrease the focus parameter
            focus=focus-5
            if focus<10:
                focus=10
            cap.set(cv.CAP_PROP_FOCUS,focus)#set focus
            print ("focus: "+str(focus))
            
    
        elif k == ord('a'):
            cap.set(cv.CAP_PROP_AUTOFOCUS,1)#autofocus ON

        elif k== ord('t'):# it will read the barcode and print the decoded barcodes.
            print("Barcode Reading Starts...")
            cropped_image = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            start = time.time()
            barcodes=pylibdmtx.decode(cropped_image,max_count=5)
            end = time.time()

            for barcode in barcodes:
                x, y , w, h = barcode.rect#barcodes pixel location information
                cv.rectangle(frame, (x+r[0],y+r[1]),((x+w)+r[0], (y+h)+r[1]), (255, 0, 0), 3)#Put rectangle

            name= "f= " +str(focus)+" Cont: " +str("%.2f"%C1)+" Exp: "+str(expo)+" dtime= " +str("%.6f"%(end-start))
            timestr = time.strftime("%Y%m%d-%H%M%S")# time information for processed image saving
            text1=str(timestr+" ")+name+" "+str(barcodes)+"\n"
            
            if len(str(barcodes))>5:
                print("BARCODE DECODED")
                f = open("C:/Users/noyan.ahmet/Desktop/python/Useful Scripts/Plate_Detection/data.txt", "a")
                f.write(text1)
                f.close()
                path="C:/Users/noyan.ahmet/Desktop/python/Useful Scripts/Plate_Detection/Decoded/"+str(timestr)+" "+str(width)+"x"+str(height)+".png"# imeage path
                cv.imwrite(path,frame) #Save the framed image
                print("image has been saved")
            else:
                print("NO BARCODE FOUND")
                path="C:/Users/noyan.ahmet/Desktop/python/Useful Scripts/Plate_Detection/Not_Decoded/"+str(timestr)+" "+str(width)+"x"+str(height)+".png"# imeage path
                cv.imwrite(path,frame) #Save the framed image
                
        elif k == ord('b'):            
            expo = expo-1
            
            if expo<-13:
                cap.set(cv.CAP_PROP_EXPOSURE, -13)
                expo=-13
            cap.set(cv.CAP_PROP_EXPOSURE,expo) 
            print("expo: " + str(expo))
    
        elif k == ord('m'):            
            expo = expo+1
            
            if expo>0:
                cap.set(cv.CAP_PROP_EXPOSURE, 0)
                expo=0
            cap.set(cv.CAP_PROP_EXPOSURE,expo) 
            print("expo: " + str(expo))

        elif k==ord('p'):

            img_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cropped_image1 = img_grey[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            mean=cv.mean(cropped_image1) 
            contrast = cropped_image1.std()
            C1=contrast/mean[0]
            print("contrast: " + str(C1))
            cv.imshow('test1',cropped_image1)
                                    
        elif k==ord('n'):
            cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
            print("Auto exposure off")
            
        elif k==ord('c'):
            cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
            print("Auto exposure on")
            expo = cap.get(cv.CAP_PROP_EXPOSURE)

        elif k == ord('f'):
            focus=95
            cap.set(cv.CAP_PROP_FOCUS,focus)
            print("focused to 8 cm")

        elif k== ord('r'):#Select ROI for Barcode
            r = cv.selectROI("select the area", frame)
            cropped_image = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            print("Selected Area= "+str(int(r[1]))+":"+str(int(r[1]+r[3]))+" , "+str(int(r[0]))+":"+str(int(r[0]+r[2])))
            cv.imshow("Cropped Image",cropped_image)

        elif k== ord('y'):#Select ROI for Plate Absence-Presence
            y1 = cv.selectROI("select the area", frame)
            template_X_distance=int(y1[0])
            template_Y_distance=int(y1[1])
            template = frame[int(y1[1]):int(y1[1]+y1[3]), int(y1[0]):int(y1[0]+y1[2])]
            images = glob.glob(r'C:\Users\noyan.ahmet\Desktop\python\Useful Scripts\Plate_Detection\Template\*.jpg')
            next_pic=len(images)+1
            template_path="C:/Users/noyan.ahmet/Desktop/python/Useful Scripts/Plate_Detection/Template/"+str(next_pic)+".jpg"
            cv.imwrite(template_path,template)
            print("Selected Area= "+str(int(y1[1]))+":"+str(int(y1[1]+y1[3]))+" , "+str(int(y1[0]))+":"+str(int(y1[0]+y1[2])))
            cv.imshow("Template",template)

        elif k==ord('u'):#Detect Plate,Read Barcode

            #PLATE DETECTION
            main_image_gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            images = glob.glob(r'C:\Users\noyan.ahmet\Desktop\python\Useful Scripts\Plate_Detection\Template\*.jpg')
            loc=[[],[]]
            threshold=0.8 #should be 0.8 and more
            for templates in images:
                I=cv.imread(templates)
                template_gray=cv.cvtColor(I, cv.COLOR_BGR2GRAY)
                w, h = template_gray.shape[::-1]
                res = cv.matchTemplate(main_image_gray, template_gray, cv.TM_CCOEFF_NORMED)     
                #print("template NAME:"+str(templates.title)+" COMPLETED")  
                #print("template MATCHING points: "+str(np.where(res >= threshold)))
                test=np.where(res >= threshold)
                loc[0]=np.append(loc[0],test[0],axis=None)
                loc[1]=np.append(loc[1],test[1],axis=None)
                #print("Appended points: "+str(loc))
                
            print("\n")
            result=loc
            result=result[::-1]  
            #print("Max pixel location "+str(max(int(result))))
            
            #print("\n")
            #print(result)
            #print("\n")
            for pt in range(len(result[0])):
                cv.rectangle(frame, (int(result[0][pt]),int(result[1][pt])),(int((result[0][pt]+w)),int((result[1][pt]+h))), (255, 0, 0), 1)            
            
            if(len(result[0])!=0):
                cv.putText(frame,'NO PLATE',(int(result[0][pt]),int(result[1][pt]+100)),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)
                timestr = time.strftime("%Y%m%d-%H%M%S")
                path="C:/Users/noyan.ahmet/Desktop/python/Useful Scripts/Plate_Detection/NoPlate/"+str(timestr)+" "+str(width)+"x"+str(height)+".png"# imeage path
                cv.imwrite(path,frame) #Save the framed image
                print("PLATE CAN NOT FIND")
            
            #BARCODE READING
            else:
                #print("Barcode Detection Starts...")
                cropped_image = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                start = time.time()
                barcodes=pylibdmtx.decode(cropped_image,max_count=5)
                end = time.time()

                for barcode in barcodes:
                    x, y , w, h = barcode.rect#barcodes pixel location information
                    cv.rectangle(frame, (x+r[0],y+r[1]),((x+w)+r[0], (y+h)+r[1]), (255, 0, 0), 3)#Put rectangle

                name= "f= " +str(focus)+" Cont: " +str("%.2f"%C1)+" Exp: "+str(expo)+" dtime= " +str("%.6f"%(end-start))
                timestr = time.strftime("%Y%m%d-%H%M%S")# time information for processed image saving
                text1=str(timestr+" ")+name+" "+str(barcodes)+"\n"
                
                if len(str(barcodes))>5:
                    print("PLATE AND BARCODE PRESENT")
                    cv.putText(frame,'Plate and Barcode Detected',(r[0],r[1]+200),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)
                    f = open("C:/Users/noyan.ahmet/Desktop/python/Useful Scripts/Plate_Detection/data.txt", "a")
                    f.write(text1)
                    f.close()
                    path="C:/Users/noyan.ahmet/Desktop/python/Useful Scripts/Plate_Detection/Decoded/"+str(timestr)+" "+str(width)+"x"+str(height)+".png"# imeage path
                    cv.imwrite(path,frame) #Save the framed image
                    print("image has been saved")
                else:
                    print("PLATE FOUND, NO BARCODE")
                    cv.putText(frame,'Plate found, No Barcode',(r[0],r[1]+200),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)
                    path="C:/Users/noyan.ahmet/Desktop/python/Useful Scripts/Plate_Detection/Not_Decoded/"+str(timestr)+" "+str(width)+"x"+str(height)+".png"# imeage path
                    cv.imwrite(path,frame) #Save the framed image
            
            cv.imshow("Detected",frame)

        elif k == ord('q'):#Exit 
            print("done")
            break
    
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

