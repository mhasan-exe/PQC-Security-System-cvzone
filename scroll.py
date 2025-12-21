import cv2
from cvzone.HandTrackingModule import HandDetector
import time

detector = HandDetector(maxHands=2, detectionCon=0.7)

def scroll_():
    source = cv2.VideoCapture(0)
    win_name = "Video Card"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    event = None
    cooldown = 1.5
    last_action_time = 0
    move = "default"
    count = 0
    while True:
        now = time.time()
        event = None  # reset every frame
        has_frame, frame = source.read()
        if not has_frame:
            break

        hands, frame = detector.findHands(frame, draw=True, flipType=True)
        if hands:
            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1)
            count = fingers1.count(1)

        if now - last_action_time >= cooldown:
            if count == 1:
                event = "previous"
                last_action_time = now
            elif count == 2:
                event = "next"
                last_action_time = now
            if event:
                print("EVENT:", event)
        print("MOVE:", move)

        cv2.imshow(win_name, frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    source.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scroll_()
