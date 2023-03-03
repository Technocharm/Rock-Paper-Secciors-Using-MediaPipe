import cv2
import time
import os
import handtrackmod as htm
import random 

wCam, hCam = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
folderPath = "imgrps"

myList = os.listdir(folderPath)
# print(myList)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(overlayList)

pTime = 0
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]
choice = ["r","p","s"]
pScore = 0
cScore = 0
pcho=None
comp=None
winner=None
won=None
waitTime = 3
prevTime = time.time()
newTime = time.time()

def checkwin(comp,pcho):
        if pcho=="r" and comp=="p":
            return 1
        elif pcho=="p" and comp=="s":
            return 1
        elif pcho=="s" and comp=="r":
            return 1
        elif pcho==comp:
            return -1
        elif comp=="r" and pcho=="p":
            return 0
        elif comp=="p" and pcho=="s":
            return 0
        elif comp=="s" and pcho=="r":
            return 0
        


while True:
    success, img = cap.read()
    
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    cv2.line(img, (wCam // 2, 0), (wCam // 2, hCam), (0, 255, 0), 5)
    cv2.rectangle(img, (780, 160), (1180, 560), (0, 0, 255), 2)
    cv2.putText(img, "Computer :", (40, 640), cv2.FONT_HERSHEY_PLAIN, 4,(0, 250, 0), 3)
    cv2.putText(img, f'{cScore}', (460, 640), cv2.FONT_HERSHEY_PLAIN, 5,(0, 250, 0), 3)
    cv2.putText(img, "Player :", (750, 640), cv2.FONT_HERSHEY_PLAIN, 4,(0, 250, 0), 3)
    cv2.putText(img, f'{pScore}', (1050, 640), cv2.FONT_HERSHEY_PLAIN, 5,(0, 250, 0), 3)

    # h, w, c = overlayList[6].shape
    # img[10:h+10, 250:w+250] = overlayList[6]

    if waitTime - int(newTime) + int(prevTime) < 0:
        cv2.putText(img, 'Go', (860, 120), cv2.FONT_HERSHEY_PLAIN, 7,(0, 0, 255), 3)
    else:
        cv2.putText(img, f'{waitTime - int(newTime) + int(prevTime)}', (960, 120), cv2.FONT_HERSHEY_PLAIN, 7,(0, 0, 255), 3)



    if len(lmList) != 0:
        if newTime - prevTime >= waitTime:
            x, y = lmList[0][1:]
            # print(lmList)
            if 780 < x < 1180 and 160 < y < 560:
                fingers = []
                # Thumb
                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # 4 Fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # print(fingers)
                totalFingers = fingers.count(1)

                if(fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0):
                    pcho="s"
                # if(totalFingers==2):
                #     pcho="s"
                elif(totalFingers==5):
                    pcho="p"
                elif(totalFingers==0):
                    pcho="r"

                #comp choice
                comp = choice[random.randint(0, 2)]
                # print(comp,pcho)
                win=checkwin(comp,pcho)
                # print(win)
                
                # print(totalFingers) 

                if win==1:
                    cScore+=1
                    won="Computer"
                elif win==0:
                    pScore+=1
                    won="Player"
                elif win==-1:
                    won="Draw"

                if(cScore>pScore):
                    winner="Computer"
                elif(cScore<pScore):
                    winner="Player"
                else:
                    winner="DrawMatch"   

                prevTime = time.time()


    cv2.rectangle(img, (90, 500), (580, 575), (0, 255, 0), cv2.FILLED)
    # cv2.putText(img, str(totalFingers), (60, 425), cv2.FONT_HERSHEY_PLAIN,6, (255, 0, 0), 15)
    cv2.rectangle(img, (90, 50), (570, 125), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(f'WonBy: {won}'), (100, 100), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
    cv2.putText(img, str(f'Winning: {winner}'), (100, 550), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
    if comp == "r":
        h, w, c = overlayList[3].shape
        img[160:h+160, 130:w+130] = overlayList[3]
    elif comp == "p":
        h, w, c = overlayList[1].shape
        img[160:h+160, 130:w+130] = overlayList[1]
    elif comp == "s":
        h, w, c = overlayList[11].shape
        img[160:h+160, 130:w+130] = overlayList[11] 

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (1050, 70), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
    
    newTime = time.time()

    cv2.imshow("Image", img)
    # cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit(0)