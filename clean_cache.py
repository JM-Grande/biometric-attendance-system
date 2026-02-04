import os
import shutil

def clean_pycache(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            print(f"Removing {pycache_path}")
            try:
                shutil.rmtree(pycache_path)
            except Exception as e:
                print(f"Error removing {pycache_path}: {e}")
                
        for file in files:
            if file.endswith(".pyc"):
                try:
                    os.remove(os.path.join(root, file))
                except:
                    pass

if __name__ == "__main__":
    clean_pycache(".")
    print("Cleanup complete.")
