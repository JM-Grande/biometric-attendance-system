import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading

class AttendanceFrame(ctk.CTkFrame):
    def __init__(self, master, face_recognizer):
        super().__init__(master)
        self.face_recognizer = face_recognizer
        self.cap = None
        self.is_running = False
        self.loading_camera = False
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Camera Feed Label
        self.camera_label = ctk.CTkLabel(self, text="Camera Feed Loading...")
        self.camera_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Status Label Overlay (We'll just use a bottom label for simplicity)
        self.status_label = ctk.CTkLabel(self, text="Ready", font=ctk.CTkFont(size=18, weight="bold"))
        self.status_label.grid(row=1, column=0, padx=20, pady=10)

    def start_camera(self):
        if not self.is_running and not self.loading_camera:
            self.loading_camera = True
            self.camera_label.configure(text="Connecting to Camera... 📷", image=None)
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
                # Run recognition
                locations, names, ids = self.face_recognizer.process_frame(frame)
                
                # Draw boxes and names on the frame
                for (top, right, bottom, left), name in zip(locations, names):
                    
                    color = (0, 255, 0) # Green by default
                    
                    # Log Attendance if known
                    status_text = ""
                    if name != "Unknown" and ids:
                        try:
                            idx = names.index(name)
                            user_id = ids[idx]
                            
                            if user_id is not None:
                                success, msg = self.face_recognizer.db.log_attendance(user_id, name)
                                status_text = msg
                                
                                if success:
                                    color = (0, 255, 0) # Green
                                    self.status_label.configure(text=msg, text_color="#2ecc71") # Green
                                else:
                                    color = (0, 165, 255) # Orange/Yellow (BGR)
                                    self.status_label.configure(text=msg, text_color="#e67e22") # Orange

                        except ValueError:
                            pass
                    else:
                         color = (0, 0, 255) # Red for unknown
                         self.status_label.configure(text="Face Not Recognized", text_color="red")

                    # Draw visual feedback on frame
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    
                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

                # Convert to ImageTk
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
                
                self.camera_label.configure(image=imgtk, text="")
                self.camera_label.image = imgtk # Keep reference
            
            if self.is_running:
                self.after(10, self.update_camera)
