import sys
import os

def check_import(module_name):
    try:
        __import__(module_name)
        print(f"✅ {module_name} imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error importing {module_name}: {e}")
        return False

def check_project_imports():
    print("\nChecking Project Modules:")
    sys.path.append(os.getcwd())
    
    modules = [
        "core.database",
        "core.recognition",
        "ui.main_window",
        "utils.config"
    ]
    
    all_good = True
    for module in modules:
        if not check_import(module):
            all_good = False
            
    return all_good

if __name__ == "__main__":
    print("Checking Dependencies...")
    dependencies = [
        "customtkinter",
        "cv2", # opencv-python
        "face_recognition",
        "numpy",
        "PIL", # Pillow
        "supabase",
        "dotenv"
    ]
    
    deps_ok = True
    for dep in dependencies:
        if not check_import(dep):
            deps_ok = False
            
    if deps_ok:
        print("\nDependencies look good!")
        if check_project_imports():
            print("\nProject structure and imports look correct!")
            print("You can try running the app with: python main.py")
        else:
            print("\nSome project modules failed to load.")
    else:
        print("\nPlease install missing dependencies using: pip install -r requirements.txt")
