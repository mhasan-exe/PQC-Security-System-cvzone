import cv2
from cvzone.HandTrackingModule import HandDetector
detector = HandDetector(maxHands=2, detectionCon=0.7)
import mediapipe as mp
import pyautogui as pag

def capture2():
    source = cv2.VideoCapture(0)
    win_name = "Video Card"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    
    while True:
        has_frame, frame = source.read()
        hands, frame = detector.findHands(frame, draw=True, flipType=True)
        if not has_frame:
            break
        if hands:
        # Information for the first hand detected
            hand1 = hands[0]  # Get the first hand detected
            lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
            bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
            center1 = hand1['center']  # Center coordinates of the first hand
            handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        # Count the number of fingers up for the first hand
            fingers1 = detector.fingersUp(hand1)
            print(f'H1 = {fingers1.count(1)}', end=" ")  # Print the count of fingers that are up
            if fingers1.count(1)== 1 and lmList1:
                x_coord, y_coord, z_coord = lmList1[8]
                pag.moveTo(x_coord,y_coord)
            if fingers1.count(1)== 2 and lmList1:
                x_coord, y_coord, z_coord = lmList1[8]
                pag.click(x_coord,y_coord)
        # Calculate distance between specific landmarks on the first hand and draw it on the image
            length, info, frame = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], frame, color=(255, 0, 255),
                                                  scale=10)

        # Check if a second hand is detected
        if len(hands) == 2:
            # Information for the second hand
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            center2 = hand2['center']
            handType2 = hand2["type"]

            # Count the number of fingers up for the second hand
            fingers2 = detector.fingersUp(hand2)
            print(f'H2 = {fingers2.count(1)}', end=" ")
            if fingers2.count(1)== 1 and lmList2:
                x_coord, y_coord, z_coord = lmList2[8]
                pag.moveTo(x_coord,y_coord)
            if fingers1.count(1)== 2 and lmList1:
                x_coord, y_coord, z_coord = lmList2[8]
                pag.click(x_coord,y_coord)
            # Calculate distance between the index fingers of both hands and draw it on the image
            length, info, frame = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], frame, color=(255, 0, 0),
                                                      scale=10)

        print(" ")  # New line for better readability of the printed output


        cv2.imshow(win_name, frame)

        # Exit on ESC key
        if cv2.waitKey(1) & 0xFF == 27:
            break

    source.release()
    cv2.destroyAllWindows()


# Only run this file standalone
if __name__ == "__main__":
    capture2()
