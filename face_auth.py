import cv2
from cvzone.FaceDetectionModule import FaceDetector
import dlib
import numpy as np
import pickle
import customtkinter as ctk

# ================= MODELS =================
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1(
    "dlib_face_recognition_resnet_model_v1.dat"
)

detector = FaceDetector()

# ================= STORAGE =================
EMB_FILE = "embeddings.pkl"
known_faces = {}

def load_embeddings():
    global known_faces
    try:
        with open(EMB_FILE, "rb") as f:
            known_faces = pickle.load(f)
    except:
        known_faces = {}

def save_embeddings():
    with open(EMB_FILE, "wb") as f:
        pickle.dump(known_faces, f)

# ================= RECOGNITION =================
def get_embedding(face_img):
    face_img = np.ascontiguousarray(face_img, dtype=np.uint8)
    h, w, _ = face_img.shape
    rect = dlib.rectangle(0, 0, w - 1, h - 1)
    shape = predictor(face_img, rect)
    emb = face_rec_model.compute_face_descriptor(face_img, shape)
    return np.array(emb)

def recognize_face(embedding, threshold=0.6):
    best_name = "Unknown"
    min_dist = float("inf")

    for name, known_emb in known_faces.items():
        dist = np.linalg.norm(embedding - known_emb)
        if dist < min_dist:
            min_dist = dist
            best_name = name

    return best_name if min_dist < threshold else "Unknown"

# ================= UI POPUP =================
def ask_username():
    result = {"name": None}

    def submit():
        result["name"] = entry.get()
        popup.destroy()

    popup = ctk.CTk()
    popup.geometry("300x150")
    popup.title("Verify User")

    entry = ctk.CTkEntry(popup, placeholder_text="Enter name")
    entry.pack(pady=20, padx=30, fill="x")

    btn = ctk.CTkButton(popup, text="Submit", command=submit)
    btn.pack(pady=10)

    popup.mainloop()
    return result["name"]

# ================= MAIN LOOP =================
def capture():
    load_embeddings()
    cap = cv2.VideoCapture(0)

    current_name = "Unknown"
    cached_embedding = None
    cooldown = 0
    PADDING = 20

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame, faces = detector.findFaces(frame)

        if faces:
            face = faces[0]
            x, y, w, h = face["bbox"]

            x1 = max(0, x - PADDING)
            y1 = max(0, y - PADDING)
            x2 = min(frame.shape[1], x + w + PADDING)
            y2 = min(frame.shape[0], y + h + PADDING)

            roi = frame[y1:y2, x1:x2]

            if roi.size > 0:
                roi = cv2.resize(roi, (112, 112))
                rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

                if cooldown <= 0:
                    cached_embedding = get_embedding(rgb)
                    cooldown = 15
                else:
                    cooldown -= 1

                cv2.putText(
                    frame,
                    current_name,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

        cv2.imshow("Face Verification", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r') and cached_embedding is not None:
            current_name = recognize_face(cached_embedding)
            print("[VERIFY]", current_name)

            if current_name == "Unknown":
                name = ask_username()
                if name:
                    known_faces[name] = cached_embedding
                    save_embeddings()
                    current_name = name

        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ================= RUN =================
if __name__ == "__main__":
    capture()
