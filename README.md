# CivicEye AI - Smart City Surveillance System

**Assignment Choice:** Assignment 1 (AI Vision / City Surveillance)  
**Role:** Full Stack Developer Intern Assignment

![Project Banner](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge) ![Tech](https://img.shields.io/badge/Tech-Node.js%20%7C%20Python%20%7C%20YOLOv8-blue?style=for-the-badge)

## Project Overview
**CivicEye AI** is a web application designed to automate the detection of civic governance issues from street-level video footage.

The system allows users to upload a short video (recorded via mobile) of a street. It processes the footage using **Computer Vision (YOLOv8)** to detect and flag issues such as **Heavy Traffic Congestion** or **Public Overcrowding**.

### Demo Preview
![Demo Preview](assets/demo.gif)
*Above: The web interface analyzing a street video.(takes about 2 min 30 sec to analyze the video)
if video not loaded, please see it in assets folder*

---

## Screenshots

| Upload Interface | AI Analysis Result | Annotated Video Feed |
|:---:|:---:|:---:|
|<img width="2237" height="1310" alt="Screenshot 2025-12-11 154011" src="https://github.com/user-attachments/assets/064752c7-ea57-4902-92e0-689ffecdcb62" />|<img width="2239" height="1244" alt="Screenshot 2025-12-10 233026" src="https://github.com/user-attachments/assets/9d0ab6de-5c88-4b1e-96f6-aef1fa671a78" />|<img width="921" height="1181" alt="Screenshot 2025-12-11 153905" src="https://github.com/user-attachments/assets/415c8433-3b35-4934-b645-850b94ad8eda" />|

---

## How It Works (The Logic)
This project uses a **Microservices-inspired architecture** to combine the speed of Node.js with the AI capabilities of Python.

### 1. The Architecture
* **Frontend:** Pure HTML/JS/CSS (No frameworks, as per requirements). Handles file uploads and status polling.
* **Backend:** **Node.js (Express)** serves as the orchestrator. It manages file storage (`Multer`) and spawns a child process to run the AI script.
* **AI Engine:** **Python + YOLOv8**. The Python script receives the video path, runs the object detection model, and returns a JSON summary to Node.js via `stdout`.

### 2. The Intelligence (Logic Fix)
A common pitfall in object detection is **"Overcounting"**. If a car stays in the frame for 10 seconds (300 frames), a standard counter detects it 300 times.
* **My Solution:** Instead of summing detections, I implemented an **Average-Per-Frame** logic.
    * `Total Cars Detected / Total Frames = Average Cars on Road`
* **Civic Issue Trigger:**
    * If `Avg Persons > 5` → Flag as **"Public Overcrowding"**.
    * If `Avg Vehicles > 8` → Flag as **"Heavy Traffic Congestion"**.

---

## Tech Stack
* **Backend:** Node.js, Express.js, Child Process
* **AI/ML:** Python 3, Ultralytics YOLOv8, OpenCV
* **Frontend:** HTML5, CSS3 (Modern UI), Vanilla JavaScript
* **Tools:** Git, Multer (File Handling)

---

## Installation & Setup

### Prerequisites
* Node.js installed
* Python 3 installed
* Git

### Step 1: Clone the Repo
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd city-surveillance-app
