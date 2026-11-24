
import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

def calculate_distance(point1, point2):
    return math.sqrt(
        (point2.x - point1.x) ** 2 +
        (point2.y - point1.y) ** 2
    )

def detect_gesture(landmarks):

    thumb_tip = landmarks[4]
    index_tip = landmarks[8]

    index_base = landmarks[5]
    pinky_base = landmarks[17]

    finger_distance = calculate_distance(
        thumb_tip, index_tip
    )

    palm_width = calculate_distance(
        index_base, pinky_base
    )

    if palm_width == 0:
        return "Neutral"

    normalized_distance = finger_distance / palm_width

    if normalized_distance < 0.35:
        return "PINCH - DECREASE"

    elif normalized_distance > 0.85:
        return "SPREAD - INCREASE"

    else:
        return "NEUTRAL"


cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(
            frame, cv2.COLOR_BGR2RGB
        )

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            for hand in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

                gesture = detect_gesture(
                    hand.landmark
                )

                cv2.putText(
                    frame,
                    gesture,
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

        cv2.imshow("GestureSense - Gesture Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
