
import cv2
import mediapipe as mp
import subprocess
import time

CAMERA_ID = 0
SMOOTHING = 0.35
SENSITIVITY = 3.5
CLICK_COOLDOWN = 0.8
MODEL_PATH = "/home/huzaifa/Code/Others/models/hand_landmarker.task"
def ydotool(*args):
    subprocess.run(
        ["ydotool", *args],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
def move_mouse(dx, dy):
    ydotool(
        "mousemove",
        "-x", str(int(dx)),
        "-y", str(int(dy)))
def left_click():
    ydotool("click", "0xC0")
def draw_hand(frame, hand, width, height):
    connections = (
        mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS)
    for connection in connections:
        start = hand[connection.start]
        end = hand[connection.end]
        p1 = (
            int(start.x * width),
            int(start.y * height))
        p2 = (
            int(end.x * width),
            int(end.y * height) )
        cv2.line(frame, p1, p2, (0, 255, 0), 2)
    for point in hand:
        x = int(point.x * width)
        y = int(point.y * height)
        cv2.circle(
            frame,
            (x, y),
            4,
            (0, 0, 255),
            -1)
cap = cv2.VideoCapture(CAMERA_ID)
if not cap.isOpened():
    print("Could not open camera.")
    exit()
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode


options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=RunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)


previous_x = None
previous_y = None

two_hands_active = False
last_click = 0


with HandLandmarker.create_from_options(options) as landmarker:

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = landmarker.detect(image)

        hands = result.hand_landmarks
        hand_count = len(hands)


        # Draw detected hands
        for hand in hands:

            draw_hand(
                frame,
                hand,
                width,
                height
            )


        #two hand logic

        if hand_count >= 2:
            previous_x = None
            previous_y = None
            if not two_hands_active:
                now = time.time()
                if now - last_click > CLICK_COOLDOWN:
                    left_click()
                    last_click = now
                two_hands_active = True
            cv2.putText(
                frame,
                "TWO HANDS - CLICK",
                (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )


        # one hand logic
        elif hand_count == 1:
            two_hands_active = False
            hand = hands[0]
            fingertip = hand[8]
            target_x = fingertip.x
            target_y = fingertip.y
            if previous_x is None:

                previous_x = target_x
                previous_y = target_y


            dx = (
                target_x - previous_x
            ) * width * SMOOTHING * SENSITIVITY

            dy = (
                target_y - previous_y
            ) * height * SMOOTHING * SENSITIVITY

            if abs(dx) > 0.3 or abs(dy) > 0.3:

                move_mouse(dx, dy)

                previous_x += (
                    dx / (width * SMOOTHING * SENSITIVITY)
                )

                previous_y += (
                    dy / (height * SMOOTHING * SENSITIVITY))
            cv2.putText(
                frame,
                "ONE HAND - MOVE",
                (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2)
        # noting
        else:
            previous_x = None
            previous_y = None
            two_hands_active = False
        cv2.putText(
            frame,
            "ESC to quit",
            (30, height - 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2)
        cv2.imshow(
            "Virtual Mouse",
            frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
