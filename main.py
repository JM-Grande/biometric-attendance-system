import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Importing UI...")
from ui.main_window import MainWindow
print("UI Imported.")

if __name__ == "__main__":
    print("Initializing Application...")
    try:
        app = MainWindow()
        print("Main Loop Starting...")
        app.mainloop()
    except Exception as e:
        print(f"CRASHED: {e}")
        import traceback
        traceback.print_exc()
    input("Press Enter to exit...")
