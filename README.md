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

# Smart Traffic Management - Citizen Safety Website

## Overview

The **Smart Traffic Management & Citizen Safety** website is designed to provide efficient and intelligent traffic solutions while ensuring citizen security. It integrates features such as chatbot assistance, shake detection for emergency alerts, multilingual support, and interactive navigation to police stations.

## Features

### 1. **Multilingual Support**

- Users can switch between multiple languages, including English, Hindi, Tamil, and Bengali.
- Implemented using an API-based dynamic translation system.

### 2. **Chatbot Assistance**

- A chatbot is integrated into the website, accessible via a floating button.
- Uses an external API for responses.
- Appears as a dropdown when clicked.

### 3. **Shake Detection for Emergencies**

- Detects sudden movements using the device's accelerometer.
- Triggers an emergency siren and alerts when shaking is detected.

### 4. **Find Nearby Police Stations**

- Users can access a locator page to find the nearest police stations.
- Uses an interactive map for easy navigation.

### 5. **Dark Mode & Theming**

- Users can toggle between light and dark modes.
- Customizable colors with Tailwind CSS.

### 6. **Modern UI/UX**

- Responsive design with Tailwind CSS.
- Animated elements using GSAP for smooth transitions.

## File Structure

```
📁 project-root
│── index.html (Main webpage)
│── locator.html (Police station locator)
│── chatbot.html (Standalone chatbot page)
│── styles.css (Custom styling)
│── shake-detector.js (Emergency shake detection)
│── chatbot.js (Handles chatbot functionality)
│── README.md (This file)
```

## How to Run

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/smart-traffic-management.git
   ```
2. Navigate to the project directory:
   ```sh
   cd smart-traffic-management
   ```
3. Open `index.html` in a web browser.

## Dependencies

- **Tailwind CSS** (for styling)
- **GSAP** (for animations)
- **Leaflet.js** (for map-based police station locator)

## Future Enhancements

- Integration of AI-based traffic monitoring.
- Improved chatbot with voice interaction.
- Real-time location tracking for emergency services.

## Credits

Developed by Team Traiffique
Selva Akash Ajay Varsan Krishna Chelliah Hariharan S Akshara V.



