from flask import Flask, request, jsonify, send_file
import cv2
import os
from ultralytics import YOLO
import uuid
import numpy as np

app = Flask(__name__)

# Create an upload folder for input and output videos
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load YOLO model
yolo_model = YOLO('yolov8n.pt')  # Ensure you have the YOLOv8 weights file

# Traffic signal images
green_signal = cv2.imread('green_signal.png')
yellow_signal = cv2.imread('yellow_signal.png')
red_signal = cv2.imread('red_signal.png')

# Resize traffic signal images to fit in the frame
if green_signal is not None:
    green_signal = cv2.resize(green_signal, (50, 50))
if yellow_signal is not None:
    yellow_signal = cv2.resize(yellow_signal, (50, 50))
if red_signal is not None:
    red_signal = cv2.resize(red_signal, (50, 50))

# List of vehicle classes to detect (YOLO's default vehicle class IDs)
vehicle_classes = [2, 5, 7, 3]  # car, bus, truck, motorcycle
emergency_vehicle_class = 10  # Assuming class 10 is for emergency vehicles

# Define a congestion threshold
CONGESTION_THRESHOLD = 19  # Tighter spacing in pixels to consider congestion

# Minimum time a signal must stay
MIN_SIGNAL_TIME = 5  # Minimum time for each signal (in seconds)

# Function to detect congestion
def detect_congestion(results, frame, congestion_threshold=CONGESTION_THRESHOLD):
    vehicle_centers = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        class_id = int(box.cls[0])

        if class_id in vehicle_classes:
            vehicle_centers.append((center_x, center_y))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    vehicle_centers.sort(key=lambda v: v[1])
    spacings = [vehicle_centers[i + 1][1] - vehicle_centers[i][1] for i in range(len(vehicle_centers) - 1)]
    avg_spacing = np.mean(spacings) if spacings else float('inf')
    vehicle_count = len(vehicle_centers)
    
    return avg_spacing < congestion_threshold, avg_spacing, vehicle_count

# Function to manage traffic signals with synchronization
def dynamic_signal_timing(vehicle_count, avg_spacing):
    if vehicle_count > 15 or avg_spacing < 25:
        return 30, 5, 10  # High congestion: longer green, standard yellow, shorter red
    elif vehicle_count > 5:
        return 20, 5, 15  # Moderate congestion
    else:
        return 10, 5, 20  # Low congestion

# Function to detect emergency vehicles
def detect_emergency_vehicle(results):
    return any(int(box.cls[0]) == emergency_vehicle_class for box in results[0].boxes)

# Function to display traffic signal images on the frame
def display_signal(frame, action):
    x, y = 50, 50
    signal_img = {'Green': green_signal, 'Yellow': yellow_signal, 'Red': red_signal}.get(action, red_signal)
    if signal_img is not None:
        frame[y:y + signal_img.shape[0], x:x + signal_img.shape[1]] = signal_img
    cv2.putText(frame, f"Signal: {action}", (x, y + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Function to process the video with stable signal durations
def process_uploaded_video(video_path, output_path="output_video.mp4"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    signal_state = "Red"
    green_duration, yellow_duration, red_duration = 10, 5, 20
    frame_counter = 0
    signal_time = {"Green": 0, "Yellow": 0, "Red": 0}  # Track time spent on each signal

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = yolo_model.predict(frame, verbose=False)
        is_congested, avg_spacing, vehicle_count = detect_congestion(results, frame)
        emergency_detected = detect_emergency_vehicle(results)

        # Print logic about vehicle density and signal times
        print(f"Frame {frame_counter}:")
        print(f"  Vehicle Count: {vehicle_count}")
        print(f"  Congested: {is_congested}, Avg Spacing: {avg_spacing}")
        if emergency_detected:
            print("  Emergency Vehicle Detected! Signal set to Green.")
            green_duration, yellow_duration, red_duration = 30, 5, 10
            signal_state = "Green"
        else:
            green_duration, yellow_duration, red_duration = dynamic_signal_timing(vehicle_count, avg_spacing)
            print(f"  Dynamic Signal Timings - Green: {green_duration}s, Yellow: {yellow_duration}s, Red: {red_duration}s")

        # Adjust signal change based on elapsed time and the minimum signal duration
        if signal_state == "Green":
            signal_time["Green"] += 1 / fps  # Increment time for Green signal
            if signal_time["Green"] >= green_duration - MIN_SIGNAL_TIME:
                if frame_counter % (green_duration + yellow_duration + red_duration) < green_duration:
                    signal_state = "Yellow"
                    print(f"  Signal Changed to Yellow after {signal_time['Green']:.2f}s of Green.")
                    signal_time["Green"] = 0  # Reset green signal time
        elif signal_state == "Yellow":
            signal_time["Yellow"] += 1 / fps  # Increment time for Yellow signal
            if signal_time["Yellow"] >= yellow_duration:
                signal_state = "Red"
                print(f"  Signal Changed to Red after {signal_time['Yellow']:.2f}s of Yellow.")
                signal_time["Yellow"] = 0  # Reset yellow signal time
        elif signal_state == "Red":
            signal_time["Red"] += 1 / fps  # Increment time for Red signal
            if signal_time["Red"] >= red_duration:
                if frame_counter % (green_duration + yellow_duration + red_duration) < red_duration:
                    signal_state = "Green"
                    print(f"  Signal Changed to Green after {signal_time['Red']:.2f}s of Red.")
                    signal_time["Red"] = 0  # Reset red signal time

        # Output details about signal changes
        print(f"  Current Signal: {signal_state} - Green Time: {signal_time['Green']:.2f}s, Yellow Time: {signal_time['Yellow']:.2f}s, Red Time: {signal_time['Red']:.2f}s")

        display_signal(frame, signal_state)
        out.write(frame)
        frame_counter += 1

    cap.release()
    out.release()
    return output_path

@app.route('/process-video', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(video_path)
    output_path = process_uploaded_video(video_path)
    return jsonify({"output_video_url": output_path})

if __name__ == "__main__":
    app.run(debug=True)
