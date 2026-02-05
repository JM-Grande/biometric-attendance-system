import cv2
import numpy as np
import os
import pickle
import logging
from typing import List, Tuple, Optional, Any
from core.database import DatabaseManager

class FaceRecognizer:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.logger = logging.getLogger(__name__)
        
        # Initialize LBPH Face Recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Load Haar Cascade for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        if self.face_cascade.empty():
            self.logger.error("Failed to load Haar Cascade classifier.")
        
        self.known_face_names: dict[int, str] = {}  # Map ID -> Name
        self.is_trained: bool = False
        self.model_path: str = "trained_faces.yml"
        self.labels_path: str = "labels.pickle"
        
        # Enterprise Config
        # Lower is stricter (0 is perfect match). > 65 is usually Unknown.
        self.confidence_threshold: int = 65 
        
        self.load_known_faces()

    def load_known_faces(self) -> None:
        """Load trained model from disk if it exists."""
        if os.path.exists(self.model_path) and os.path.exists(self.labels_path):
            try:
                self.recognizer.read(self.model_path)
                with open(self.labels_path, 'rb') as f:
                    self.known_face_names = pickle.load(f)
                self.is_trained = True
                self.logger.info("Loaded trained face model successfully.")
            except Exception as e:
                self.logger.error(f"Error loading model: {e}")
                # We do not call train_model() here as we don't have raw images on disk to retrain from
        else:
            self.logger.warning("No trained model found. Starting fresh.")

    def process_frame(self, frame: np.ndarray) -> Tuple[List[Tuple[int, int, int, int]], List[str], List[Optional[int]]]:
        """
        Process a single frame for face recognition.
        Returns:
            face_locations: List of (top, right, bottom, left)
            face_names: List of recognized names
            face_ids: List of recognized user IDs (or None)
        """
        if frame is None:
            return [], [], []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )

        face_locations = []
        face_names = []
        face_ids = []

        for (x, y, w, h) in faces:
            # Convert to CSS order: top, right, bottom, left
            face_locations.append((y, x+w, y+h, x)) 
            
            name = "Unknown"
            user_id = None

            if self.is_trained:
                roi_gray = gray[y:y+h, x:x+w]
                try:
                    # Predict gives label (id) and confidence (distance)
                    label_id, confidence = self.recognizer.predict(roi_gray)
                    
                    if confidence < self.confidence_threshold: 
                        name = self.known_face_names.get(label_id, "Unknown")
                        user_id = label_id
                    # Else remains Unknown
                    
                except Exception as e:
                    self.logger.debug(f"Prediction error: {e}")
            
            face_names.append(name)
            face_ids.append(user_id)
            
        return face_locations, face_names, face_ids

    def register_new_face(self, frames: List[np.ndarray], name: str, employee_id: str) -> Tuple[bool, str]:
        """
        Extract faces from multiple frames, update the model, and save to DB.
        
        Args:
            frames: List of image arrays (BGR)
            name: User's full name
            employee_id: Unique Employee ID
            
        Returns:
            Success (bool), Message (str)
        """
        if not frames:
            return False, "No frames provided"

        # 1. Save user to DB to get a unique internal ID
        # This prevents ID conflicts and ensures we have a valid key for the recognizer
        success, result = self.db.add_user_placeholder(name, employee_id)
        
        if not success:
            return False, result # result is error message
            
        new_db_id = result # result is the integer ID
        
        collected_faces = []
        collected_ids = []
        
        self.logger.info(f"Processing {len(frames)} frames for {name} (ID: {employee_id})...")
        
        for frame in frames:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(50, 50)
            )
            
            # Use the largest face in frame
            if len(faces) > 0:
                largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
                (x, y, w, h) = largest_face
                roi_gray = gray[y:y+h, x:x+w]
                
                collected_faces.append(roi_gray)
                collected_ids.append(new_db_id)

        if len(collected_faces) < 5:
            # If we couldn't find faces in at least 5 frames, abort to avoid bad model
            return False, "Could not detect face clearly. Please try again with better lighting."

        # 2. Update the model
        try:
            # LBPH supports updating the model with new data without retraining from scratch
            self.recognizer.update(collected_faces, np.array(collected_ids))
            
            # Save updated model
            self.recognizer.save(self.model_path)
            
            # Update labels map
            self.known_face_names[new_db_id] = name
            with open(self.labels_path, 'wb') as f:
                pickle.dump(self.known_face_names, f)
                
            self.is_trained = True
            self.logger.info(f"Successfully registered {name} with {len(collected_faces)} samples.")
            return True, f"Registered {name} successfully!"
            
        except Exception as e:
            self.logger.error(f"Training error: {e}")
            return False, f"System Error during training: {str(e)}"
