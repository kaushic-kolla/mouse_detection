# -*- coding: utf-8 -*-

import cv2
import numpy as np
import MouseTracing as mt
import time
import autopy

########### CONSTANTS ###################################
cWidth, cHeight = 640, 480
frameR = 100
smoothen = 8

pTime=0
plX, plY  = 0 , 0
clX, clY = 0 , 0

############################################################

capture = cv2.VideoCapture(0)
capture.set(3, cWidth)
capture.set(4, cHeight)
pTime = 0
handLocator = mt.handDetector(maxHands=1)
sWidth, sHeight = autopy.screen.size()

while(1):

     #1.get the image
    success,hand = capture.read()
    hand = handLocator.getHands(hand)
    fingerlist, bbox = handLocator.findPosition(hand)


    #2. scan the edges of index and middle finger
    if len(fingerlist)!=0:
        x1, y1 = fingerlist[8][1:]
        
        x2, y2 = fingerlist[12][1:]

        #print(x1,y1,x2,y2)
        #3. check with fingerArray

        fingerArray = handLocator.fingerCount()
        cv2.rectangle(hand, (frameR, frameR), (cWidth - frameR, cHeight - frameR),
                      (230, 230, 250), 2)
        #4. making the mouse move if only index finger is shown
        if fingerArray[1]==1 and fingerArray[2]==0:

        #5. using np to get the values


            x3 = np.interp(x1, (frameR, cWidth-frameR), (0, sWidth))
            y3 = np.interp(y1, (frameR, cHeight-frameR), (0, sHeight))

            #6. controlling the frame sensitivity
            clX = plX + (x3 - plX) / smoothen
            clY = plY + (y3 - plY) / smoothen
             #7. making the mouse move using autopy
            autopy.mouse.move(sWidth-clX,clY)
            cv2.circle(hand, (x1, y1), 15,  (234, 221, 202), cv2.FILLED)
            plX, plY = clX, clY
        #8. condition for clicking, if only index and middle finger is open
        if fingerArray[1] == 1 and fingerArray[2] ==1 :
            # 9. satisfying the condition
            length, hand, lineInfo = handLocator.getDistance(8, 12, hand)
    
            if length < 40:
                cv2.circle(hand, (lineInfo[4], lineInfo[5]), 15, (251, 206, 177), cv2.FILLED)
                autopy.mouse.click()




    #10. controlling the framerate
    cur = time.time()
    fps = 1/(cur - pTime)
    pTime = cur
    cv2.putText(hand,str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    #12. Display
    cv2.imshow("Image", hand)
    cv2.waitKey(1)
