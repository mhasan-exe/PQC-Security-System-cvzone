import customtkinter as ctk
from PIL import Image
import os
import time
import cv2
from cvzone.HandTrackingModule import HandDetector

from func import typewriter
from face_auth import capture
from pqc import pqc_
from gesture_control import capture2


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1200x670")
app.title("POST-QUANTUM Security System")

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "images")



left_panel = ctk.CTkFrame(app, width=450, corner_radius=30)
left_panel.pack(side="left", fill="both")

right_panel = ctk.CTkFrame(app, corner_radius=30)
right_panel.pack(side="right", fill="both", expand=True)


logo_img = Image.open(os.path.join(IMAGE_PATH, "logo.jpg"))
logo_image = ctk.CTkImage(logo_img, size=(400, 300))

logo_label = ctk.CTkLabel(left_panel, image=logo_image, text="")
logo_label.place(relx=0.5, rely=0.4, anchor="center")

ctk.CTkLabel(
    left_panel, text="POST-QUANTUM",
    font=("Segoe UI", 35, "bold")
).place(relx=0.5, rely=0.65, anchor="center")

ctk.CTkLabel(
    left_panel, text="Security System",
    font=("Segoe UI", 25, "bold")
).place(relx=0.5, rely=0.75, anchor="center")


slides = [
    "Slide 1: Face Detection Module",
    "Slide 2: Face Recognition & Verification",
    "Slide 3: Hand Tracking Module",
    "Slide 4: Gesture Control System",
    "Slide 5: PQC Logic Layer",
    "Slide 6: CustomTkinter Interface",
    "Slide 7: Real-World System Approach"
]

slide_index = 0
1
slide_frame = ctk.CTkFrame(
    right_panel, corner_radius=20,
    fg_color="#222222", width=700, height=200
)
slide_frame.pack(pady=(50, 10))
slide_frame.pack_propagate(False)

slide_label = ctk.CTkLabel(
    slide_frame, text=slides[slide_index],
    font=("Segoe UI", 25, "bold")
)
slide_label.pack(expand=True)

gesture_indicator = ctk.CTkLabel(
    right_panel, text="", font=("Segoe UI", 20, "bold"),
    text_color="cyan"
)
gesture_indicator.pack(pady=(20, 0))

intro_text = ctk.CTkLabel(right_panel, text="", font=("Segoe UI", 15))
intro_text.pack(pady=(10, 0))

typewriter(
    intro_text,
    "This Interface is made by M Hasan to showcase an AI-driven security system with gesture control and PQC logic."
)


face_icon = ctk.CTkImage(Image.open(os.path.join(IMAGE_PATH, "face.png")), size=(32, 32))
lock_icon = ctk.CTkImage(Image.open(os.path.join(IMAGE_PATH, "lock.png")), size=(32, 32))
bio_icon  = ctk.CTkImage(Image.open(os.path.join(IMAGE_PATH, "bio.png")),  size=(32, 32))

ctk.CTkButton(
    app, text="Face", image=face_icon,
    fg_color="red", hover_color="#950606",
    width=260, height=50,
    command=capture
).place(relx=0.8, rely=0.9, anchor="center")

ctk.CTkButton(
    app, text="Biometric/Gesture", image=bio_icon,
    fg_color="#32CD32", hover_color="#39e75f",
    width=260, height=50,
    command=capture2
).place(relx=0.5, rely=0.9, anchor="center")

ctk.CTkButton(
    app, text="Post-Quantum Mechanics", image=lock_icon,
    fg_color="purple", hover_color="#A865C9",
    width=520, height=50,
    command=pqc_
).place(relx=0.65, rely=0.8, anchor="center")


detector = HandDetector(
    maxHands=1,
    detectionCon=0.65,    
    minTrackCon=0.6
)

gesture_cooldown = 1.0   
last_action_time = 0
last_gesture = None
gesture_frames = 0       

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)      


def smooth_slide_change(new_index):
    global slide_index
    slide_index = new_index % len(slides)
    slide_label.configure(text=slides[slide_index])

def gesture_loop():
    global last_action_time, last_gesture, gesture_frames

    cap.grab()  
    ret, frame = cap.read()
    if not ret:
        app.after(40, gesture_loop)
        return

    hands, _ = detector.findHands(frame, draw=False)
    now = time.time()
    event = None

    if hands:
        fingers = detector.fingersUp(hands[0])

        if fingers == [0, 0, 0, 0, 0]:
            event = "next"
        elif fingers[1] and fingers[2] and not fingers[3]:
            event = "previous"
        elif all(fingers):
            event = "reset"
        else:
            event = None

        if event == last_gesture:
            gesture_frames += 1
        else:
            gesture_frames = 1
            last_gesture = event


        if (
            event
            and gesture_frames >= 2
            and (now - last_action_time) >= gesture_cooldown
        ):
            last_action_time = now
            gesture_frames = 0

            if event == "next":
                gesture_indicator.configure(text="Next →")
                smooth_slide_change(slide_index + 1)

            elif event == "previous":
                gesture_indicator.configure(text="← Previous")
                smooth_slide_change(slide_index - 1)

            elif event == "reset":
                gesture_indicator.configure(text="Reset")
                smooth_slide_change(0)

    else:
        last_gesture = None
        gesture_frames = 0
        gesture_indicator.configure(text="")

    app.after(40, gesture_loop)  




app.after(200, gesture_loop)
app.mainloop()

cap.release()
cv2.destroyAllWindows()
