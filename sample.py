import cv2
import numpy as np
import dlib
import pickle
from cvzone.FaceDetectionModule import FaceDetector
import face_recognition

detector = FaceDetector()
pa = 25
cap = cv2.VideoCapture(0)
win_name = "Face Reg"
cv2.namedWindow(win_name,cv2.WINDOW_KEEPRATIO)
while True:
    has_frame, frame = cap.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    if not has_frame:
        break
    frame, bboxs = detector.findFaces(frame)
    if len(bboxs) > 0:
        bbox1 = bboxs[0]
        x, y, w, h = bbox1["bbox"]
        print(x,y,w,h)
        cv2.putText(
                    frame,
                    "Hasan",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )
        x1 = max(0, x - pa)
        y1 = max(0, y - pa)
        x2 = min(frame.shape[1], x + w + pa)
        y2 = min(frame.shape[0], y + h + pa)

        if (x2 - x1) <= 0 or (y2 - y1) <= 0:
            continue

        crop = frame[y1:y2,x1:x2]
        resized = cv2.resize(crop,(128,128))
        cv2.imshow("ROI",resized)
        encode = face_recognition.face_encodings(resized)
        print(encode)
    cv2.imshow(win_name,frame)
    if cv2.waitKey(1) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()