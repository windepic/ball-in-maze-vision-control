# ball-in-maze-vision-control
Vision-Guided Autonomous Ball-in-Maze Navigation System
# Ball-in-Maze Vision Control: YOLOv8 + Path Planning + Arduino Interface

This repository presents the core computer vision and control modules I developed as part of a group-based final-year project at the University of Bristol. The project involved real-time autonomous navigation of a metallic silver ball across a maze using visual closed-loop feedback.

> Note: This repository includes only the modules I personally contributed to, including object detection, path planning, and serial communication.

---

## Project Overview

The system detects a metallic ball and maze holes using YOLOv8, extracts a user-drawn path on the maze surface via HSV + edge detection, samples it using arc-length techniques, and sends control instructions to an Arduino-connected dual-servo platform.

- YOLOv8 detection for dynamic ball and holes objects
- Path extraction via HSV + Canny edge detection
- START/FINISH detection  via geometric heuristics to orient the path from start to end
- Arc-length-based resampling of contours to generate navigation points
- Real-time serial control to an Arduino for maze tilt

---


## File Structure

```
.
├── main.py             - Sample integration code for module testing  
├── yolo_detector.py    - YOLOv8-based detection of metallic ball and holes  
├── path_planning.py    - Path extraction and arc-length sampling  
├── serial_comm.py      - Serial communication to Arduino  
├── requirements.txt    - Python dependency list  
└── assets/             - Demo images or result screenshots  
```
