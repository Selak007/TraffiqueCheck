import cv2
import torch
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import os
from flask import Flask, Response, render_template, jsonify

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load YOLOv8 model
yolo_model = YOLO("yolov8n.pt")  # Using YOLOv8 nano for efficiency

# Initialize DeepSORT tracker
tracker = DeepSort(max_age=30, n_init=3, nms_max_overlap=1.0)

# Open video stream
video_path = "videoplayback (online-video-cutter.com).mp4"
cap = cv2.VideoCapture(video_path)

accident_detected = False
accident_count = 0
prev_positions = {}  # Store previous positions of tracked vehicles
frame_counter = 0  # Counter to track frames since last accident detection
accident_threshold = 50  # Number of frames to wait before detecting another accident

app = Flask(__name__)

# Generate frames for streaming
def generate_frames():
    global accident_detected, accident_count, prev_positions, frame_counter
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run YOLO detection
        results = yolo_model(frame)
        detections = []
        for result in results:
            for box in result.boxes.data:
                x1, y1, x2, y2, conf, cls = box.tolist()
                if conf > 0.5:  # Confidence threshold
                    detections.append(([x1, y1, x2, y2], conf, int(cls)))
        
        # Update tracker
        tracks = tracker.update_tracks(detections, frame=frame)
        current_positions = {}
        
        # Store results without drawing bounding boxes
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            ltrb = track.to_ltrb()
            x1, y1, x2, y2 = map(int, ltrb)
            
            # Store current position
            current_positions[track_id] = (x1, y1, x2, y2)
        
        # Accident Detection Logic
        if frame_counter >= accident_threshold:  # Only detect after 50 frames have passed
            accident_detected = False  # Reset flag for each frame
            for track_id, (x1, y1, x2, y2) in current_positions.items():
                if track_id in prev_positions:
                    px1, py1, px2, py2 = prev_positions[track_id]
                    
                    # Check sudden stop (drastic reduction in movement) and impact
                    if abs(x1 - px1) < 3 and abs(y1 - py1) < 3:
                        for other_id, (ox1, oy1, ox2, oy2) in current_positions.items():
                            if other_id != track_id:
                                # Ensure tighter collision detection
                                overlap_x = max(0, min(x2, ox2) - max(x1, ox1))
                                overlap_y = max(0, min(y2, oy2) - max(y1, oy1))
                                overlap_area = overlap_x * overlap_y
                                if overlap_area > 0.95 * ((x2 - x1) * (y2 - y1)):
                                    if not accident_detected:  # Prevent multiple detections
                                        accident_detected = True
                                        accident_count += 1
                                        frame_counter = 0  # Reset frame counter after accident is detected
                                        break
                if accident_detected:
                    break
        
        # Increment frame counter
        if not accident_detected:
            frame_counter += 1
        
        prev_positions = current_positions.copy()
        
        if accident_detected:
            cv2.putText(frame, "⚠️ ACCIDENT DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def stats():
    return jsonify({"accident_count": accident_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

