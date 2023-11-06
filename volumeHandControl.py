import cv2
import time
import numpy as np
import handtrackingmodule as htm
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##########################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volRange = (volume.GetVolumeRange())
minVol = volRange[0]
maxVol = volRange[1]
print(volRange)
##########################

####################
wCam, hCam = 640, 480
####################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

cTime = 0
pTime = 0
bar = 0
volBar = 400

detector = htm.handDetector(detection_Con=0.7)

while True:
    success, img = cap.read()

    if not success:
        break

    detector.findHands(img)
    lmList = detector.find_Position(img, draw=False)
    
    if len (lmList) != 0:
        #index 4 = thumb
        #index 8 = finger next to thumb
        thumbX, thumbY = lmList[4][1], lmList[4][2]
        indexX, indexY = lmList[8][1], lmList[8][2]
        centerX, centerY = (thumbX + indexX)//2 , (thumbY + indexY)//2

        cv2.circle(img, (thumbX, thumbY), 12, (255,0,255), cv2.FILLED)
        cv2.circle(img, (indexX, indexY), 12, (255,0,255), cv2.FILLED)
        cv2.circle(img, (centerX, centerY), 12, (255,0,255), cv2.FILLED)
        cv2.line(img, (thumbX, thumbY), (indexX, indexY), (255,0,255),3)
        
        lineLength = np.sqrt(  (thumbX - indexX)**2 + (thumbY - indexY)**2  )//1

        vol = np.interp(lineLength, [50,200], [minVol,maxVol])
        volBar = np.interp(lineLength, [50,200], [400,150])
        volPercentage = np.interp(lineLength, [50,200],[0,100])
        volume.SetMasterVolumeLevel(vol, None)


        cv2.rectangle(img, (50,150), (85,400), (255,0,0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85,400), (255,0,0), cv2.FILLED)
        cv2.putText(img, f'{int(volPercentage)}%', (50, 430), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),1)
    else:
        currentVol = np.interp(volume.GetMasterVolumeLevel() , [-65.25 , 0], [0,100])
        #print(volume.GetMasterVolumeLevel())
        #print(currentVol)
        cv2.putText(img, f'{int(currentVol)}%', (50, 430), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps: {int(fps)}', (20,40), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(1)


