from ultralytics import YOLO
import numpy as np
import cv2

class YoloDetector:
    def __init__(self, ball_model_path="best.pt", hole_model_path="hole.pt"):
        self.ball_model = YOLO(ball_model_path)
        self.hole_model = YOLO(hole_model_path)
        self.known_holes = []
        self.hole_labels = []
        self.next_hole_id = 1

    def detect_ball(self, frame, conf_threshold=0.25):
        results = self.ball_model.predict(source=frame, conf=conf_threshold, device=0, verbose=False)[0]
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            if self.ball_model.names[cls_id] == 'ball' and conf > conf_threshold:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                return (cx, cy)
        return None

    def detect_holes(self, frame, conf_threshold=0.3, distance_thresh=25):
        results = self.hole_model.predict(source=frame, conf=conf_threshold, device=0, verbose=False)
        raw_detections = []
        for r in results:
            for box in r.boxes:
                if r.names[int(box.cls[0])] == "hole":
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                    r_est = int(max(x2 - x1, y2 - y1) / 2)
                    raw_detections.append((cx, cy, r_est))
        return raw_detections
