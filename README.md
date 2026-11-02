# AI Surveillance System with Weapon Detection

An AI-powered real-time surveillance system that detects weapons using a YOLOv8 deep learning model.  
The system monitors webcam footage, detects motion, identifies weapons, and sends email alerts with captured images.

---

## Features

- Real-time weapon detection using YOLOv8
- Motion detection to reduce unnecessary computation
- Face detection using Haar Cascade
- Email alert system when a weapon is detected
- Automatic screenshot capture of detected threat
- Alarm sound notification
- Lightweight and efficient real-time system

---

## Output Images (weapon detected)

<img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/70c9c70d-fbbf-4e9a-a9c3-3c59a519c678" />

---

## Technologies Used

- Python
- OpenCV
- YOLOv8 (Ultralytics)
- Haar Cascade Face Detection
- SMTP Email Alerts

---

## System Architecture

Camera Feed
↓  
Motion Detection
↓  
Face Detection
↓
YOLOv8 Weapon Detection
↓  
Threat Confirmation
↓  
Alert System (Email + Alarm)

---

 
## Results
 
Metrics at the final epoch (50), on the validation set:
 
| Metric | Value |
|---|---|
| mAP@50 | **0.770** |
| mAP@50-95 | 0.498 |
| Precision | 0.711 |
| Recall | 0.762 |
| Best F1 (all classes) | 0.72 at confidence 0.327 |
 
Per class:
 
| Class | AP@50 |
|---|---|
| Firearm (`senjata_api`) | 0.934 |
| Knife (`senjata_tajam`) | 0.606 |
 
![Training curves](metrics/results.png)
 
![Normalized confusion matrix](metrics/confusion_matrix_normalized.png)
 
All curves and raw per-epoch numbers are in [`metrics/`](metrics/).
 

## Dataset

The weapon detection model was trained using a custom dataset in YOLO format containing multiple weapon classes including:

- Gun
- Knife
- Handgun
- Shotgun
- Sniper
- Sword
- Grenade Launcher



## File Structure

```

AI-Surveillance-System-Weapon-Detection
│
├── dataset/
│   └── Weapon Detection.v1.yolov8/
│       ├── train
│       ├── valid
│       ├── test
│       └── data.yaml
│
├── models/
│   └── best.pt
│
├── detect_webcam.py
├── train_model.py
├── haarcascade_frontalface_default.xml
├── requirements.txt
├── README.md
├── .gitignore
└── test.png

```



Dataset format:

```
train/images
train/labels
valid/images
valid/labels
test/images
test/labels
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Surveillance-System-Weapon-Detection.git
cd AI-Surveillance-System-Weapon-Detection
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the System

```bash
python detect_webcam.py
```

Press **ESC** to exit.

---

## Training the Model

```bash
yolo detect train data=data.yaml model=yolov8n.pt epochs=50
```

The trained model will be saved in:

```
runs/detect/train/weights/best.pt
```

---

## Author

Suyash Pawar  
B.Tech CSE Student
