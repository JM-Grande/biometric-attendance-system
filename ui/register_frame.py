import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
import time

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, face_recognizer):
        super().__init__(master)
        self.face_recognizer = face_recognizer
        self.cap = None
        self.is_running = False
        self.loading_camera = False
        self.current_frame_data = None
        self.capture_frames = []
        self.is_capturing = False
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Side: Camera
        self.camera_frame = ctk.CTkFrame(self)
        self.camera_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.camera_label = ctk.CTkLabel(self.camera_frame, text="Camera Feed")
        self.camera_label.pack(expand=True, fill="both", padx=10, pady=10)

        # Right Side: Form
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ns")
        
        self.title_label = ctk.CTkLabel(self.form_frame, text="Register New User", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20, padx=20)
        
        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Full Name")
        self.name_entry.pack(pady=10, padx=20, fill="x")
        
        self.id_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Employee ID")
        self.id_entry.pack(pady=10, padx=20, fill="x")
        
        self.capture_btn = ctk.CTkButton(self.form_frame, text="Start Training (Look at Camera)", command=self.start_capture_sequence)
        self.capture_btn.pack(pady=20, padx=20, fill="x")
        
        self.progress_bar = ctk.CTkProgressBar(self.form_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.pack_forget() # Hide initially
        
        self.status_label = ctk.CTkLabel(self.form_frame, text="")
        self.status_label.pack(pady=10)

    def start_camera(self):
        if not self.is_running and not self.loading_camera:
            self.loading_camera = True
            self.camera_label.configure(text="Initializing Video Feed... 📷")
            threading.Thread(target=self._init_camera, daemon=True).start()

    def _init_camera(self):
        try:
            new_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Faster on Windows
            if new_cap.isOpened():
                self.cap = new_cap
                self.is_running = True
                self.after(0, self.update_camera)
            else:
                self.after(0, lambda: self.camera_label.configure(text="Camera Failed to Open"))
        except Exception as e:
             self.after(0, lambda: self.camera_label.configure(text=f"Camera Error: {e}"))
        finally:
            self.loading_camera = False

    def stop_camera(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def update_camera(self):
        if self.is_running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame_data = frame.copy()
                
                # If capturing for training, collect frames
                if self.is_capturing:
                    # Add visual indicator (Green Border)
                    cv2.rectangle(frame, (0,0), (frame.shape[1], frame.shape[0]), (0, 255, 0), 10)
                
                # Convert to ImageTk
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 300))
                
                self.camera_label.configure(image=imgtk, text="")
                self.camera_label.image = imgtk
            
            if self.is_running:
                self.after(20, self.update_camera)

    def start_capture_sequence(self):
        name = self.name_entry.get()
        emp_id = self.id_entry.get()
        
        if not name or not emp_id:
            self.status_label.configure(text="Please fill all fields", text_color="red")
            return
            
        if self.current_frame_data is None:
             self.status_label.configure(text="No camera feed", text_color="red")
             return

        self.capture_btn.configure(state="disabled", text="Scanning Face...")
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)
        self.status_label.configure(text="Hold still...", text_color="orange")
        
        # Start capture thread
        threading.Thread(target=self._capture_frames_thread, args=(name, emp_id), daemon=True).start()

    def _capture_frames_thread(self, name, emp_id):
        self.is_capturing = True
        self.capture_frames = []
        target_frames = 30
        
        for i in range(target_frames):
            if not self.is_running: break
            if self.current_frame_data is not None:
                self.capture_frames.append(self.current_frame_data)
                
            # Update progress bar
            progress = (i + 1) / target_frames
            self.after(0, lambda p=progress: self.progress_bar.set(p))
            
            time.sleep(0.05) # Capture every 50ms
            
        self.is_capturing = False
        
        self.after(0, lambda: self.status_label.configure(text="Processing Model...", text_color="blue"))
        
        # Now register with collected frames
        success, msg = self.face_recognizer.register_new_face(self.capture_frames, name, emp_id)
        
        self.after(0, lambda: self._finish_registration(success, msg))

    def _finish_registration(self, success, msg):
        self.capture_btn.configure(state="normal", text="Start Training")
        self.progress_bar.pack_forget()
        
        if success:
            self.status_label.configure(text=msg, text_color="green")
            self.name_entry.delete(0, 'end')
            self.id_entry.delete(0, 'end')
        else:
            self.status_label.configure(text=f"Error: {msg}", text_color="red")
