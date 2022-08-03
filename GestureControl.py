from turtle import position
import cv2
import HandTrackingModule as htm
import numpy as np
import cv2
import time
import math
from ursina import Ursina, Entity, color, EditorCamera, Sky, Vec3, Cursor, window
import autopy
import Texture

wCam, hCam = 640, 480
wScr, hScr = autopy.screen.size()
frameR = 70
smoothening = 3

pLen, cLen = 0, 0

pSize, cSize, netSize = 0, 0, 0
sizeSmooth = 5
sizeDiffer = 0.02

rotSmooth = 5
# rotSpeed = 0.2

# x=1, y=2, z=3
rotOrient = 2
rotIsChange = False

plocX, plocY = 0, 0
clocX, clocY = 0, 0

pTime = 0
cTime = 0

detector = htm.handDetector(maxHands=2, detectionCon=0.5)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

app = Ursina()
Cursor(texture="cursor(1).png")
window.fullscreen = True
# wWin, hWin = 10, 10

cube = Entity(model="cube", texture="./Basic1.png",
              scale=1, double_sided=True)

Sky()

# cursor = Entity(model="circle", color=color.red, scale=0.1)

EditorCamera()


def VirtualButton(texture, color, scale, position, function_name_on_click):
    button = Entity(model="quad", texture=texture, color=color,
                    scale=scale, position=Vec3(position[0], position[1], position[2]))


def update():
    global pTime, plocX, plocY, pLen, cLen, pSize, cSize, rotOrient, rotIsChange, netSize
    success, img = cap.read()
    img = detector.findHands(img)
    noHands = detector.get_number_of_hands(img)
    lmList, bbox = detector.findPosition(img, draw=True)
    if noHands == 2:
        lmList2, bbox2 = detector.findPosition(img, handNo=1, draw=True)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)

    # print(noHands)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        if noHands == 1:
            if fingers[1] == 1 and fingers[2] == 0:
                # 5. Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                try:
                    plocX, plocY = clocX, clocY
                    autopy.mouse.move(wScr - clocX, clocY)
                except:
                    autopy.mouse.move(wScr - plocX, plocY)
                    plocX, plocY = clocX, clocY
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            if fingers[1] == 1 and fingers[2] == 1:
                lengthC, img, lineInfo = detector.findDistance(
                    8, 12, lmList, lmList, img, r=7)
                if lengthC < 10:
                    autopy.mouse.click()

        if noHands == 2:
            finger2 = detector.fingersUp(handNo=1)
            # print(fingers, finger2)

            if fingers[1] == 1 and fingers[2] == 1:
                if finger2[1] == 1 and finger2[2] == 1:

                    if fingers[3] == 0 and finger2[3] == 0:
                        if fingers[4] == 0 and finger2[4] == 0:
                            length1, img1, info1 = detector.findDistance(
                                8, 12, lmList, lmList, img, (255, 0, 0), (0, 255, 0), r=7)

                            length2, img2, info2 = detector.findDistance(
                                8, 12, lmList2, lmList2, img, (255, 0, 0), (0, 255, 0), r=7)
                            px1, py1 = info1[4], info1[5]
                            px2, py2 = info2[4], info2[5]
                            # print(px1, py1, '\n', px2, py2, '\n')
                            cx, cy = (px1 + px2) // 2, (py1 + py2) // 2
                            cv2.line(img, (px1, py1), (px2, py2),
                                     (255, 0, 255), 3)
                            cv2.circle(img, (cx, cy), 7,
                                       (255, 0, 0), cv2.FILLED)
                            # cSize = math.hypot(px2 - px1, py2 - py1)
                            length = math.hypot(px2 - px1, py2 - py1)
                            # if pSize == 0:
                            #     pSize = cSize
                            #     print("It came here")
                            # else:
                            #     if cSize - pSize > sizeSmooth or pSize - cSize > sizeSmooth:
                            #         print(int(cSize), ' ', int(pSize))
                            #         netSize = int(pSize) - int(cSize)
                            #         cube.scale = cube.scale * \
                            #             (netSize/sizeDiffer)
                            #         print(netSize)
                            #         pSize = cSize

                            # # print(netSize, pSize, cSize)
                            # # print(cube.scale[0])
                            # cube.scale = Vec3(
                            #     cube.scale[0] + netSize, cube.scale[1] + netSize, cube.scale[2] + netSize)

                            cube.scale = length/100

                            # if pSize == 0:
                            #     pSize = cSize
                            #     print("It came here")
                            # else:
                            #     if cSize - pSize > sizeSmooth or pSize - cSize > sizeSmooth:
                            #         netSize = int(cSize) - int(pSize)
                            #         print(int(netSize), int(
                            #             cSize), ' ', int(pSize))
                            #         pSize = cSize
                            #         cube.scale = (
                            #             cube.scale + (netSize*sizeDiffer))
                            #         # cube.scale = Vec3(
                            #         #     cube.scale[0] + (netSize*sizeDiffer), cube.scale[1] + (netSize*sizeDiffer), cube.scale[2] + (netSize*sizeDiffer))
            if fingers[1] == 1 and finger2[1] == 1:
                if finger2[2] == 0 and finger2[2] == 0:
                    # if fingers[0] == 0 and finger2[0] == 0:
                    if fingers[3] == 0 and finger2[3] == 0:
                        if fingers[4] == 0 and finger2[4] == 0:
                            cLen, i1, ifo1 = detector.findDistance(
                                8, 8, lmList, lmList2, img, (255, 0, 0), (0, 255, 0), r=7)
                            if pLen == 0:
                                pLen = cLen
                            else:
                                if cLen - pLen > rotSmooth or pLen - cLen > rotSmooth:
                                    netLen = cLen - pLen
                                    # print(netLen)
                                    if rotOrient == 1:
                                        cube.rotation_x = cube.rotation_x + netLen
                                    if rotOrient == 2:
                                        cube.rotation_y = cube.rotation_y + netLen
                                    if rotOrient == 3:
                                        cube.rotation_z = cube.rotation_z + netLen
                                    pLen = cLen

            if fingers[1] == 1 and fingers[4] == 1:
                if fingers[2] == 0 and fingers[3] == 0:
                    if finger2[1] == 1 and finger2[4] == 1:
                        if finger2[2] == 0 and finger2[3] == 0:
                            if rotIsChange == False:

                                if rotOrient == 2 and rotIsChange == False:
                                    rotOrient = 3
                                    rotIsChange = True

                                if rotOrient == 3 and rotIsChange == False:
                                    rotOrient = 1
                                    rotIsChange = True

                                if rotOrient == 1 and rotIsChange == False:
                                    rotOrient = 2
                                    rotIsChange = True
                                print(rotOrient)
                            # else:
                                # pLen, cLen = 0
            else:
                rotIsChange = False

        if noHands == 0:
            plen, clen = 0
            pSize, cSize = 0
            rotIsChange = False

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


app.run()
