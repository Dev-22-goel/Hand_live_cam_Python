import cv2
import time 
import os
import HandTrackingModule as htm

wCam, hCam= 640, 480

cap=cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3,wCam)
cap.set(4,hCam)

folderpath="Fingers"
mylist=os.listdir(folderpath)
# print(mylist)

overlaylist=[]

for imgpath in mylist:
    image=cv2.imread(f'{folderpath}/{imgpath}')
    # print((f'{folderpath}/{imgpath}'))


    overlaylist.append(image)

# print(len(overlaylist))
ptime=0

detector = htm.handDetector(detectionCon=0.5)

tipids=[4,8,12,16,20]

while True:
    success, img=cap.read()
    img=detector.findHands(img)

    lmlist=detector.findPosition(img, draw=False)
    # print(lmlist)

    fingers=[]
    if len(lmlist) !=0:

        #thumb
        if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
           fingers.append(1)
        else:
            fingers.append(0)

        #4 fingers
        for id in range(1,5):
                if lmlist[tipids[id]][2] < lmlist[tipids[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        # print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers)


        h,w,c= overlaylist[totalFingers-1].shape
        img[0:h, 0:w]=overlaylist[totalFingers-1] 

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,10, (255, 0, 0), 25)  

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img, f'FPS: {int(fps)}',(400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),3 )

    cv2.imshow("Image", img)
    cv2.waitKey(1)