import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.main_window import MainWindow
except ImportError as e:
    logging.error(f"Failed to import UI components: {e}")
    sys.exit(1)

if __name__ == "__main__":
    logging.info("Initializing Biometric Attendance System...")
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        logging.critical(f"Application crashed: {e}", exc_info=True)
        input("Press Enter to close...")
