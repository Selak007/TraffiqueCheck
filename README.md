# TraffiqueCheck

## Overview

TraffiqueCheck is a smart traffic management system that includes:

- **Accident Detection:** Detects accidents using YOLO and DeepSORT.
- **Vehicle Counting & Traffic Management:** Counts vehicles and adjusts traffic signals dynamically.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required Python packages:
  ```bash
  pip install flask opencv-python numpy torch ultralytics deep_sort_realtime
  ```
- YOLOv8 Model Weights: Download and place `yolov8n.pt` and `yolov8n-int8.pt` in the project folder.
- Required signal images (`green_signal.png`, `yellow_signal.png`, `red_signal.png`) for traffic management.

---

## 1. Accident Detection

### Description

This module uses YOLO and DeepSORT tracking to detect accidents in video streams. It runs a Flask server to visualize detections.

### Running the Script

```bash
export FLASK_APP=accidentdetection.py
flask run --host=0.0.0.0 --port=5000
```

### How It Works

- The script loads a video (`videoplayback.mp4`).
- YOLO detects vehicles and DeepSORT tracks them.
- If a vehicle suddenly stops and overlaps with another vehicle, an accident is detected.
- A message is displayed on the video when an accident is detected.

### API Endpoints

- `http://127.0.0.1:5000/` → Dashboard
- `http://127.0.0.1:5000/video_feed` → Live video stream
- `http://127.0.0.1:5000/stats` → JSON response with accident count

### Expected Output

- A browser window displaying live video feed with accident detection alerts.
- JSON response: `{ "accident_count": 3 }`

---

## 2. Vehicle Counter & Traffic Signal Management

### Description

This module detects and counts vehicles, then dynamically adjusts traffic signals based on congestion levels.

### Running the Script

```bash
export FLASK_APP=vehiclecounter.py
flask run --host=0.0.0.0 --port=5001
```

### How It Works

- Users upload a video via the `/process-video` API.
- YOLO detects vehicles, and spacing between them determines congestion.
- Traffic lights dynamically change based on vehicle density and emergency vehicle detection.
- The processed video is saved in `./outputs/`.

### API Endpoints

- `POST /process-video` → Upload a video and get a processed video URL.
  - **Request:** Upload video file.
  - **Response:** `{ "output_video_url": "./outputs/output_video.mp4" }`

### Expected Output

- Processed video showing vehicles and dynamically changing traffic signals.
- Console logs showing congestion levels and traffic light changes.

---

## Using Postman for Video Processing

1. Open **Postman**.
2. Create a **new POST request** to:
   ```
   http://127.0.0.1:5001/process-video
   ```
3. In the **Body** tab, select **form-data**.
4. Add a new key:
   - **Key:** `video`
   - **Type:** File
   - **Value:** (Select the video file from your system)
5. Click **Send**.
6. The response will return a JSON object with the processed video URL:
   ```json
   {
     "output_video_url": "./outputs/output_video.mp4"
   }
   ```

---

## Contributing

Fork the repository and submit pull requests for improvements.

## License

MIT License

