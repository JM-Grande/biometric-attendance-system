import cv2
import numpy as np
import os
import pickle
from utils.config import Config

class FaceRecognizer:
    def __init__(self, db_manager):
        self.db = db_manager
        # Use LBPH (Local Binary Patterns Histograms) Face Recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.known_face_names = {}  # Map ID -> Name
        self.known_face_ids = []
        self.is_trained = False
        self.model_path = "trained_faces.yml"
        self.labels_path = "labels.pickle"
        
        # Enterprise Config
        self.confidence_threshold = 65 # Lower is stricter (0 is perfect match). > 65 is Unknown.
        
        self.load_known_faces()

    def load_known_faces(self):
        """Load trained model if exists, otherwise train from DB."""
        if os.path.exists(self.model_path) and os.path.exists(self.labels_path):
            try:
                self.recognizer.read(self.model_path)
                with open(self.labels_path, 'rb') as f:
                    self.known_face_names = pickle.load(f)
                self.is_trained = True
                print("Loaded trained face model.")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.train_model()
        else:
            print("No trained model found. Starting fresh.")
            self.train_model()

    def train_model(self):
        """Train the recognizer with faces from the database."""
        # For this lightweight version, we rely on the saved .yml model.
        # Re-training from scratch would require storing all raw images on disk.
        pass

    def process_frame(self, frame):
        """
        Process a single frame for face recognition.
        Returns locations, names, ids found in frame.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        face_locations = []
        face_names = []
        face_ids = []

        for (x, y, w, h) in faces:
            face_locations.append((y, x+w, y+h, x)) # CSS order: top, right, bottom, left
            
            name = "Unknown"
            user_id = None

            if self.is_trained:
                roi_gray = gray[y:y+h, x:x+w]
                try:
                    # Predict gives label (id) and confidence (distance)
                    label_id, confidence = self.recognizer.predict(roi_gray)
                    
                    # Confidence check
                    if confidence < self.confidence_threshold: 
                        name = self.known_face_names.get(label_id, "Unknown")
                        user_id = label_id
                    else:
                        name = "Unknown"
                except Exception as e:
                    print(e)
            
            face_names.append(name)
            face_ids.append(user_id)
            
        return face_locations, face_names, face_ids

    def register_new_face(self, frames, name, employee_id):
        """
        Extract faces from multiple frames, train model, and save to DB.
        frames: List of image arrays (BGR)
        """
        if not frames:
            return False, "No frames provided"

        # 1. Save user to DB to get an ID (or check if exists)
        success, msg_or_id = self.db.add_user_placeholder(name, employee_id)
        
        if not success:
            return False, msg_or_id # msg_or_id is error message here
            
        new_db_id = msg_or_id
        
        collected_faces = []
        collected_ids = []
        
        print(f"Processing {len(frames)} frames for {name}...")
        
        for frame in frames:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
            
            # Use the largest face in frame
            if len(faces) > 0:
                # Find largest face
                largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
                (x, y, w, h) = largest_face
                roi_gray = gray[y:y+h, x:x+w]
                
                collected_faces.append(roi_gray)
                collected_ids.append(new_db_id)

        if len(collected_faces) < 5:
            return False, "Could not detect face clearly in enough frames. Please try again."

        # 2. Update the model
        try:
            self.recognizer.update(collected_faces, np.array(collected_ids))
            
            # Save updated model
            self.recognizer.save(self.model_path)
            
            # Update labels map
            self.known_face_names[new_db_id] = name
            with open(self.labels_path, 'wb') as f:
                pickle.dump(self.known_face_names, f)
                
            self.is_trained = True
            return True, f"Registered {name} with {len(collected_faces)} samples!"
            
        except Exception as e:
            return False, f"Training error: {e}"
