import cv2
from yolo_detector import YoloDetector
from path_planning import sample_contour_by_arc_length
from serial_comm import ArduinoController

cap = cv2.VideoCapture(0)
detector = YoloDetector()
arduino = ArduinoController()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    ball = detector.detect_ball(frame)
    holes = detector.detect_holes(frame)

    if ball:
        print("Ball detected at:", ball)
        arduino.send_angle(1, -1)  # Sample angle

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
