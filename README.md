# Gesture & Biometric Security System (Python)

A Python-based security system that combines **face recognition**, **hand gesture control**, and a **slide-based UI** to demonstrate modern human–computer interaction and access control concepts.

This project is designed as a **functional prototype**, focusing on computer vision, interaction logic, and system design rather than presentation-only demos.

please take a moment to read this and my story behind this tool!

## 🚀 Features
- Face recognition using **dlib**
- Hand gesture detection for navigation
- Slide-based UI controlled via gestures
- Modular Python structure
- Real-time camera processing

---
```
## 🧠 Technologies Used
- Python 3.11.x
- OpenCV
- dlib
- MediaPipe
- NumPy
- Customtkinter
- visual studio(required to get cmake)
- visual studio code
- cmake(required to build dlib)
```
---

## 📦 Requirements
install python 3.11.x and then use pip to install requirements.txt file by 
```python -m pip install -r requirements.txt```

## Insutructions after installing python and requirements.txt

> ⚠️ Note:  
> - `dlib` may require **CMake** and **Visual C++ Build Tools** on Windows.  
> - It is highly recommended to use a **virtual environment**.

---

## 🛠️ Installation

1. **Create & activate virtual environment**
```bash
python -m venv stem-env #this one creates new enviroment
stem-env\Scripts\activate   # Windows (this line opens virtual enviroment)
```
2. **Download the face recognition model**
   https://www.kaggle.com/datasets/sergiovirahonda/shape-predictor-68-face-landmarksdat
   
## Running
```python new_ui.py```

after running you will see a normal ctk interface where you can:

1. Open hand in front of interface to reset slides to first one

2. slowly close hand to move to next slides

3. open middle and index fingers to go to previous slides

4. open hand gesture system to see live hand tracking + distance between your index fingers of both hands

5. in the live tracking module, open only your index finger to move mouse with it

6. press Ecs key to close the window

7. open face module next and press r to process and verify people , it will not verify until r is pressed again which means people's name will not change unless r is pressed

8. Now you can move towards Post Quantum Module to check a secure string guesser, and security level predictor!

9. Caution: ALL module either have exit button or require escape to be pressed to exit, and the slides can't work after access is passed to another window and needs the program to be restarted for security issues!

10. Do Let me know if you have a question or an issue in the program! 

11. That's all , happy coding! 

### Troubleshooting
1. Visual studio desktop cmake tool (not vs code) is required to make wheels for dlib face recognition model
2. make sure to download the shape predictor file from the link above
3. numpy newer version can't process dlib face recognition model properly so only use from the requirements.txt file!
4. if you open any module, the camera can't work for slides so that program don't crash hence needs a restart!
5. opencv course is also available on opencv-university website to learn what is happening here, I will share my certificate here as well!
That's all but to support me , just hear out my story😊
----------------------------
🎯 Project Motivation & Story

This project was built under real pressure, limited time, and limited support.
It represents:
learning by building instead of copying

choosing engineering depth over visual shortcuts

persistence even when results were not publicly recognized

While this system started as a competition project, it now stands as proof of skill, growth, and direction.

Not every effort receives immediate validation —
but every real build compounds.
-- and in the end, this project broke me because pushing this into a small competition and refining it for months just turned into
a celebration without me , a celebration where I was the audience and thats when I have decided to make it open-source for everyone😊

👤 Author

Hasan

Python Developer | Computer Vision Enthusiast

📸 Instagram: @mhasan.exe

📱 WhatsApp: 03358207180

📥E-mail: muhammadhasanm44@gmail

📌 Disclaimer
This project is for educational and demonstration purposes only.
It is not intended for real-world security deployment without further testing and hardening.
