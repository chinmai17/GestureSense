# GestureSense – AI-Powered Hand Gesture Laptop Controller

GestureSense is a Python-based computer vision project that allows users to control laptop brightness and system volume using real-time hand gestures.

It uses a webcam to detect hand movements and recognize gestures, providing a touch-free way to interact with laptop settings.

## Features

- **Real-time hand tracking:** Detects hands using MediaPipe.
- **Brightness control:** Use your left hand to increase or decrease screen brightness.
- **Volume control:** Use your right hand to increase or decrease system volume.
- **Gesture recognition:** Pinch to decrease and spread to increase settings.
- **Gesture lock/unlock:** Raise your pinky finger to toggle gesture controls.
- **Live visual feedback:** Displays detected hands, gestures and lock status.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Webcam capture and image processing |
| MediaPipe | Hand landmark detection |
| NumPy | Numerical computing dependency |
| Pycaw | Windows system volume control |
| Screen Brightness Control | Screen brightness adjustment |

## Project Architecture

1. Webcam captures live video.
2. OpenCV processes each frame.
3. MediaPipe detects 21 landmarks on each hand.
4. Gesture recognition calculates normalized fingertip distance.
5. The application identifies the required action.
6. Python libraries adjust brightness or volume.

## Gesture Controls

| Hand gesture | Action |
|---|---|
| Left-hand pinch | Decrease brightness |
| Left-hand spread | Increase brightness |
| Right-hand pinch | Decrease volume |
| Right-hand spread | Increase volume |
| Raise pinky | Lock/unlock controls |
| Press Q | Exit application |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/GestureSense.git
cd GestureSense
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment (Windows PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python main.py
```

## Requirements

- Windows laptop
- Python 3.11 recommended
- Webcam
- Supported display brightness controls
- Working audio output device

## Project Structure

```text
GestureSense/
│
├── main.py
├── system_control.py
├── hand_detection.py
├── gesture_detection.py
├── camera_test.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Future Enhancements

- Add custom hand gestures.
- Improve gesture recognition accuracy.
- Add a graphical user interface.
- Support configurable gesture sensitivity.
- Add gesture-based media and presentation controls.

## Learning Outcomes

Through this project, I explored computer vision, real-time image processing, hand landmark detection, gesture recognition, Python libraries and Windows system automation.

## Author

**Chinmai S Patil**

GitHub: https://github.com/chinmai17

Portfolio: https://chinmai-portfolio-ten.vercel.app

---

**GestureSense – Control your laptop with your hands!**
