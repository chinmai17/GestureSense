
import cv2

# Open the default webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Webcam not detected!")
    exit()

print("Webcam started successfully!")

while True:
    success, frame = camera.read()

    if not success:
        print("Unable to read camera frame")
        break

    # Mirror the webcam
    frame = cv2.flip(frame, 1)

    # Display webcam
    cv2.imshow("GestureSense Camera Test", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
