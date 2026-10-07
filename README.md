# AI_cursor_controller


A minimalist computer-vision virtual mouse controlled using a webcam and hand tracking.

## How It Works

The camera detects hands using **MediaPipe Hand Landmarker**.

* **One hand detected** → move the mouse using the index fingertip.
* **Two hands detected** → perform a left click.
* **No hands detected** → mouse stops.

Mouse movement is controlled through `ydotool`, making it compatible with Linux Wayland.

## Requirements

* Python 3.14
* OpenCV
* MediaPipe 1.1.0
* NumPy
* ydotool
* Webcam

Install Python packages:

```bash
pip install opencv-python mediapipe numpy
```

Install ydotool:

```bash
sudo apt install ydotool
```

## Model

Download the MediaPipe hand landmark model and place it at:

```text
models/hand_landmarker.task
```

## Run

Start the ydotool daemon and make sure the socket is accessible:

```bash
sudo systemctl start ydotool
sudo chown $USER:$USER /run/user/1000/.ydotool_socket
```

Then run:

```bash
python3 main.py
```

Press **ESC** to exit.

## Controls

| Hands detected | Action     |
| -------------- | ---------- |
| 0              | Nothing    |
| 1              | Move mouse |
| 2              | Left click |

## Main Settings

```python
SMOOTHING = 0.35
SENSITIVITY = 3.5
CLICK_COOLDOWN = 0.8
```

Increase `SENSITIVITY` for faster cursor movement.

## Pipeline

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Hand Landmarker
   ↓
Hand Count / Index Fingertip
   ↓
Gesture Decision
   ↓
ydotool
   ↓
Mouse
```
YEP I LOVE WRITING CODE NOT readms.md so let AI handle that part