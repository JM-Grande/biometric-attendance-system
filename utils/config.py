import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL", "your-project-url")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-key")
    USE_CLOUD = os.getenv("USE_CLOUD", "False").lower() == "true"
    
    # Paths
    DB_PATH = "attendance.db"
    
    # Appearance
    THEME_MODE = "Dark"  # System, Dark, Light
    COLOR_THEME = "blue"   # blue, green, dark-blue
    
    # Biometrics
    TOLERANCE = 0.6  # Lower is stricter
    MODEL = "hog"    # hog or cnn (cnn is slower but more accurate)
