# 📸 Enterprise Biometric Attendance System

A high-performance, offline-first attendance application featuring real-time face recognition, enterprise-grade database management, and a modern dark-mode UI.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-orange)

## ✨ Features

- **🚀 Instant Recognition**: Uses LBPH (Local Binary Patterns Histograms) for fast and efficient face matching.
- **🛡️ Enterprise Grade Registration**: Captures **30+ samples** per user in a burst sequence to ensure high accuracy across different angles.
- **⏱️ Smart Attendance**:
  - **Duplicate Prevention**: Automatically rejects duplicate check-ins for the same day.
  - **Visual Feedback**: Green/Orange/Red indicators on the live feed for instant status.
- **💾 Hybrid Database**:
  - **Offline First**: All data stored locally in SQLite (`attendance.db`).
  - **Cloud Ready**: Optional built-in support for **Supabase** sync.
- **🎨 Modern UI**: Sleek, responsive interface built with CustomTkinter.

---

## 🛠️ Installation Guide (Error-Free)

### 1. Prerequisites
*   **Python 3.10 or newer** installed.
*   *(Optional)* **Visual Studio Build Tools** (only if you plan to switch back to `dlib`, but this version works without it!).

### 2. Automatic Setup (Windows)
We have included a "One-Click" installer script.

1.  Open the folder `attendance-app`.
2.  Double-click **`run_app.bat`**.
    *   This will automatically create a virtual environment.
    *   Install all necessary libraries.
    *   Launch the application.

### 3. Manual Setup (Command Line)
If you prefer the terminal:

```powershell
# 1. Navigate to the project
cd attendance-app

# 2. Create Virtual Environment
python -m venv venv

# 3. Activate Environment
.\venv\Scripts\activate

# 4. Install Dependencies
pip install -r requirements.txt

# 5. Run the App
python main.py
```

---

## 📖 How to Use

### 1️⃣ Registering a New Employee
1.  Launch the app and navigate to the **"Register User"** tab.
2.  Enter the **Full Name** and **Employee ID**.
3.  Click **"Start Training"**.
4.  **Look at the camera**: The system will automatically capture **30 frames** (takes ~2 seconds).
    *   *Tip: Move your head slightly for better accuracy.*
5.  Wait for the "Registration Successful!" message.

### 2️⃣ Taking Attendance
1.  Navigate to the **"Take Attendance"** tab.
2.  The camera will start automatically.
3.  Simply walk in front of the camera.
    *   **Green Box**: "Welcome! Marked Present." ✅
    *   **Orange Box**: "You already took attendance today." ⚠️
    *   **Red Box**: "Unknown" (Please register). ❌

### 3️⃣ Viewing Logs
1.  Go to the **"Home"** tab.
2.  See the **Live Stats** for total users and today's attendance count.
3.  View the list of **Recent Activity**.

---

## ☁️ Cloud Sync (Optional)
To enable Cloud Sync with Supabase:
1.  Open `utils/config.py`.
2.  Set `USE_CLOUD = True`.
3.  Add your `SUPABASE_URL` and `SUPABASE_KEY`.

---

## ❓ Troubleshooting

**Q: Camera not starting?**
A: Ensure no other app (Zoom, Teams) is using the webcam.

**Q: "No module named..." error?**
A: Run `run_app.bat` again to ensure dependencies are installed.

**Q: Face not recognized?**
A: Try registering again with better lighting. The system learns from the data you give it!
