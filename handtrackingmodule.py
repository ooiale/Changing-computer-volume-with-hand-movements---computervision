import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode = False, maxHands = 2, detection_Con = 0.5, tracking_Con = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detection_Con
        self.trackingCon = tracking_Con
   
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,1
                                        ,self.detectionCon,self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils #connecting the landmarks on the hand

    def findHands(self,  img, draw = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        #print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                                self.mpHands.HAND_CONNECTIONS) #drawing marks for each hand
        return img
    
    def find_Position(self,  img, handNo=0, draw = True):
        lmList = []
        if self.result.multi_hand_landmarks: #checking if hands are there
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark): 
                #print(id,lm)
                #the coordinates are given in proportion to the size of the screen (%)
                h, w, c = img.shape #height width channel
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw and id == 0:
                    cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED) #draws a circle on the landmark of specific ID
        return lmList



def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.find_Position(img)
        if len(lmList) != 0:
            print(lmList[0])


        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

        cv2.imshow('image',img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()