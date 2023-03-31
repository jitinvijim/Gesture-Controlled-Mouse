#todo list
#figure out GPU acceleration
#implement scrolling

import cv2
import numpy as np
import HandTrackModule as htm
import time
import pyautogui
pyautogui.FAILSAFE = False
frameR = 250
smooth = 5
prevLocX, prevLocY = 0,0
currLocX, currLocY = 0,0
wCam, hCam = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = htm.handDetector(maxHands = 1)
wScr, hScr = pyautogui.size()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img) 

    if len(lmList)!=0:
         x1, y1 = lmList[8][1:]
         x2, y2 = lmList[12][1:]
         x4, y4 = lmList[4][1:]

         #print(x1,y1,x2,y2)

         fingers = detector.fingersUp()
         print(fingers)
         cv2.rectangle(img,(frameR,frameR), (wCam-frameR, hCam-frameR), (255,0,255), 2)
         
         if fingers[1]==1 and fingers[2]==0:
               
               x3 = np.interp(x1, (frameR,wCam-frameR),(0,wScr))
               y3 = np.interp(y1, (frameR,hCam-frameR), (0,hScr))
               currLocX = prevLocX +(x3-prevLocX)/smooth
               currLocY = prevLocY +(y3-prevLocY)/smooth

               pyautogui.moveTo((wScr-currLocX),currLocY)
               cv2.circle(img, (x1,y1), 12,(255,0,2555), cv2.FILLED)
               prevLocX, prevLocY=currLocX, currLocY

         if fingers[1]==1 and fingers[2]==1:
              length, img, lineInfo= detector.findDistance(8,12,img)
              #print(length)
              if length<47:
                  cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                  pyautogui.click()

         if fingers[1]==1 and fingers[0]==0:
              length, img, lineInfo= detector.findDistance(8,4,img)
              #print(length)
              if length<47:
                  cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                  pyautogui.click(button='right')
   
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2. putText(img, str(int(fps)),(70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)
    if cv2.waitKey(10) & 0xFF == ord('q'):
         break