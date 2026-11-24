
import cv2
import mediapipe as mp
import math
import time

from system_control import change_brightness, change_volume


# ---------------- CONFIGURATION ----------------

PINCH_THRESHOLD = 0.35
SPREAD_THRESHOLD = 0.85

ACTION_INTERVAL = 0.5
LOCK_COOLDOWN = 1.5

controls_locked = False
last_lock_time = 0

last_action = {
    "Left": 0,
    "Right": 0
}

# Track pinky gesture transitions
pinky_was_up = False


# ---------------- MEDIAPIPE SETUP ----------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


# ---------------- DISTANCE CALCULATION ----------------

def calculate_distance(p1, p2):
    return math.sqrt(
        (p2.x - p1.x) ** 2 +
        (p2.y - p1.y) ** 2
    )


# ---------------- GESTURE DETECTION ----------------

def detect_gesture(landmarks):

    thumb_tip = landmarks[4]
    index_tip = landmarks[8]

    index_base = landmarks[5]
    pinky_base = landmarks[17]

    palm_width = calculate_distance(
        index_base,
        pinky_base
    )

    if palm_width == 0:
        return "NEUTRAL"

    finger_distance = calculate_distance(
        thumb_tip,
        index_tip
    )

    normalized_distance = finger_distance / palm_width

    if normalized_distance < PINCH_THRESHOLD:
        return "DECREASE"

    elif normalized_distance > SPREAD_THRESHOLD:
        return "INCREASE"

    return "NEUTRAL"


# ---------------- PINKY DETECTION ----------------

def is_pinky_up(landmarks):

    pinky_tip = landmarks[20]
    pinky_middle = landmarks[18]

    return pinky_tip.y < pinky_middle.y


# ---------------- CAMERA INITIALIZATION ----------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam could not be opened.")
    raise SystemExit


# ---------------- MAIN PROGRAM ----------------

try:

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        model_complexity=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                print("Unable to read webcam frame.")
                break

            # Mirror webcam
            frame = cv2.flip(frame, 1)

            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = hands.process(rgb_frame)

            # Process detected hands
            if results.multi_hand_landmarks:

                for i, hand in enumerate(
                    results.multi_hand_landmarks
                ):

                    # Identify left or right hand
                    handedness = (
                        results.multi_handedness[i]
                        .classification[0].label
                    )

                    landmarks = hand.landmark

                    # Draw hand landmarks
                    mp_draw.draw_landmarks(
                        frame,
                        hand,
                        mp_hands.HAND_CONNECTIONS
                    )

                    current_time = time.time()

                    # -------- PINKY LOCK / UNLOCK --------

                    pinky_up = is_pinky_up(landmarks)

                    # Toggle only when pinky changes
                    # from down to up
                    if pinky_up and not pinky_was_up:

                        if (
                            current_time - last_lock_time
                            >= LOCK_COOLDOWN
                        ):

                            controls_locked = not controls_locked
                            last_lock_time = current_time

                    pinky_was_up = pinky_up

                    # -------- DETECT HAND GESTURE --------

                    gesture = detect_gesture(landmarks)

                    # -------- CONTROL SYSTEM --------

                    if not controls_locked:

                        if gesture != "NEUTRAL":

                            if (
                                current_time -
                                last_action[handedness]
                                >= ACTION_INTERVAL
                            ):

                                if handedness == "Left":

                                    if gesture == "INCREASE":
                                        change_brightness("increase")

                                    elif gesture == "DECREASE":
                                        change_brightness("decrease")

                                elif handedness == "Right":

                                    if gesture == "INCREASE":
                                        change_volume("increase")

                                    elif gesture == "DECREASE":
                                        change_volume("decrease")

                                last_action[handedness] = current_time

                    # -------- DISPLAY GESTURE --------

                    cv2.putText(
                        frame,
                        f"{handedness}: {gesture}",
                        (20, 40 + i * 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

            # -------- DISPLAY LOCK STATUS --------

            status = (
                "LOCKED" if controls_locked
                else "UNLOCKED"
            )

            status_color = (
                (0, 0, 255) if controls_locked
                else (0, 255, 0)
            )

            cv2.putText(
                frame,
                f"Controls: {status}",
                (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                status_color,
                2
            )

            cv2.putText(
                frame,
                "Press Q to Quit",
                (20, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "GestureSense - Smart Laptop Controller",
                frame
            )

            # Press Q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:

    cap.release()
    cv2.destroyAllWindows()

print("GestureSense stopped.")
