import numpy as np

class HoleManager:
    def __init__(self):
        self.known_holes = []
        self.hole_labels = []
        self.next_hole_id = 1
        self.row_thresh = 12

        # Define custom thresholds
        self.hole_detect_ranges = {
            "Hole 2": 10,
            "Hole 10": 10,
            "Hole 11": 30,
            "Hole 12": 30,
            "Hole 13": 10,
            "Hole 16": 10,
            "Hole 17": 10,
            "Hole 20": 10,
            "Hole 22": 10,
            "Hole 23": 10,
            "Hole 24": 10,
        }
        self.dangerous_holes = {"Hole 14", "Hole 15"}

    def order_holes_tblr(self, centroids):
        centroids = sorted(centroids, key=lambda p: p[1])
        rows, bucket = [], []
        for p in centroids:
            if not bucket or abs(p[1] - bucket[0][1]) < self.row_thresh:
                bucket.append(p)
            else:
                rows.append(bucket)
                bucket = [p]
        if bucket:
            rows.append(bucket)
        ordered = []
        for row in rows:
            ordered.extend(sorted(row, key=lambda p: p[0]))
        return ordered

    def label_holes(self, detections, distance_thresh=25):
        labeled = []
        ordered = self.order_holes_tblr([(x, y) for (x, y, r) in detections])
        ordered_detections = [next(det for det in detections if det[0] == x and det[1] == y) for (x, y) in ordered]

        for (x, y, r) in ordered_detections:
            for i, (kx, ky) in enumerate(self.known_holes):
                if np.hypot(x - kx, y - ky) < distance_thresh:
                    labeled.append((x, y, r, self.hole_labels[i]))
                    break
            else:
                label = f"Hole {self.next_hole_id}"
                self.next_hole_id += 1
                self.known_holes.append((x, y))
                self.hole_labels.append(label)
                labeled.append((x, y, r, label))

        return labeled

    def get_detection_range(self, label):
        return self.hole_detect_ranges.get(label, 55)

    def is_dangerous(self, label):
        return label in self.dangerous_holes
