"""from cvzone.HandTrackingModule import HandDetector
import cv2
import socket

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 9769)

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    data1 = []
    data2 = []

    if hands:
        # Hand 1
        # if len(hands) == 1:
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points

        length1, info1, _ = detector.findDistance(
            (lmList[1][0], lmList[1][1]), (lmList[5][0], lmList[5][1]), img)
        length2, info2, _ = detector.findDistance(
            (lmList[0][0], lmList[0][1]), (lmList[17][0], lmList[17][1]), img)

        # print(info1[4], info1[5])
        # print(info2[4], info2[5])

        l, info, _ = detector.findDistance(
            (info1[4], info1[5]), (info2[4], info2[5]), img)

        cx, cy = info[4], info[5]
        # print(len(lmList))
        for lm in lmList:
            data.extend([len(hands), lm[0], h - lm[1], lm[2]])
            # data1.append(lm[0], h - lm[1], lm[2])
        data1.extend(cx, cy, lmList[1][2])
        print(data1)
        # if len(hands) == 2:
        #     hand1 = hands[0]
        #     hand2 = hands[1]
        #     lmList1 = hand1["lmList"]  # List of 21 Landmark points
        #     lmList2 = hand2["lmList"]
        #     for lm1 in lmList1:
        #         for lm2 in lmList2:
        #             data.extend([lm1[0], h - lm1[1],
        #                          lm1[2], lm2[0], h - lm2[1], lm2[2]])
        sock.sendto(str.encode(str(data1)), serverAddressPort)
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
"""
try:
    from cvzone.HandTrackingModule import HandDetector
    import cv2
    import socket
except:
    import pip
    pip.main(['install', 'cvzone'])
    print("\nINSTALLED CVZONE\n")
    pip.main(['install', 'opencv-python'])
    print("\nINSTALLED OPENCV\n")
    pip.main(['install', 'mediapipe==0.8.10'])
    print("\nINSTALLED MEDIAPIPE \n")

from cvzone.HandTrackingModule import HandDetector
import cv2
import socket


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = (socket.gethostbyname(socket.gethostname()), 9769)

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    data = []

    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points

        length, info, _ = detector.findDistance(
            (lmList[4][0], lmList[4][1]), (lmList[8][0], lmList[8][1]), img)

        print(length)

        for lm in lmList:
            data.extend([lm[0], h - lm[1], lm[2]])
        data.extend([int(length)])
        sock.sendto(str.encode(str(data)), serverAddressPort)

    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
