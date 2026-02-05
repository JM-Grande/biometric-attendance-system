# 🔐 Biometric Attendance System (Enterprise Edition)

A professional-grade, offline-first attendance management system powered by Face Recognition (OpenCV LBPH).
Built with Python and CustomTkinter for a modern, responsive UI.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 Key Features

*   **⚡ Instant Recognition**: Uses highly optimized LBPH (Local Binary Patterns Histograms) for real-time face matching.
*   **📸 Smart Registration**: Captures a 30-frame burst to build a robust face model for each employee.
*   **🛡️ Duplicate Prevention**: Automatically prevents employees from clocking in twice on the same day.
*   **📊 Live Dashboard**: View real-time logs and attendance statistics.
*   **☁️ Hybrid Database**: Runs 100% offline with SQLite. Optional Supabase cloud sync built-in.
*   **🎨 Dark Mode UI**: Professional, eye-friendly interface.

---

## 🚀 Quick Start (Windows)

No technical skills required. Just run the launcher.

1.  **Clone or Download** this repository.
2.  Double-click **`run_app.bat`**.
    *   This will automatically create a virtual environment, install dependencies, and launch the app.

---

## 🛠️ Manual Installation

If you prefer the command line:

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

---

## 📖 User Guide

### 1. Register a New User
*   Navigate to the **"Register User"** tab.
*   Enter **Full Name** and **Employee ID**.
*   Click **"Start Training"**.
*   Look at the camera. The system will capture **30 frames** (approx. 1.5s) to learn your face.
*   Wait for the "Success" message.

### 2. Take Attendance
*   Navigate to the **"Take Attendance"** tab.
*   The camera will activate.
*   Simply walk in front of the camera.
*   **Green Box**: Attendance Logged! ✅
*   **Orange Box**: You have already clocked in today. ⚠️
*   **Red Box**: Unknown Face. ❌

### 3. View Logs
*   The **Home** dashboard shows the last 10 records and total count for the day.

---

## ⚙️ Configuration

Check `utils/config.py` to customize:
*   **`THEME_MODE`**: "System", "Dark", or "Light".
*   **`USE_CLOUD`**: Set to `True` to enable Supabase syncing.
*   **`SUPABASE_URL`**: Your cloud database credentials.

---

## ❓ Troubleshooting

**Camera not starting?**
*   Ensure no other app (Zoom, Teams) is using the webcam.
*   If you have multiple cameras, edit `ui/register_frame.py` and change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`.

**"Null Bytes" Error?**
*   This has been fixed in the latest release. Ensure you are using the clean files from this repo.

---

## 🏗️ Tech Stack
*   **GUI**: CustomTkinter
*   **Computer Vision**: OpenCV (opencv-contrib-python)
*   **Database**: SQLite3
*   **Language**: Python 3.10+
