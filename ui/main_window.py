import customtkinter as ctk
from .home_frame import HomeFrame
from .register_frame import RegisterFrame
from .attendance_frame import AttendanceFrame
from core.database import DatabaseManager
from core.recognition import FaceRecognizer
from utils.config import Config

ctk.set_appearance_mode(Config.THEME_MODE)
ctk.set_default_color_theme(Config.COLOR_THEME)

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Biometric Attendance System")
        self.geometry("1000x600")

        # Initialize Core Systems
        self.db_manager = DatabaseManager()
        self.face_recognizer = FaceRecognizer(self.db_manager)

        # Layout configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Navigation Frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.nav_label = ctk.CTkLabel(self.navigation_frame, text="Attendance App",
                                      compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.nav_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.register_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Register User",
                                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                             command=self.register_button_event)
        self.register_button.grid(row=2, column=0, sticky="ew")

        self.attendance_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Take Attendance",
                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                               command=self.attendance_button_event)
        self.attendance_button.grid(row=3, column=0, sticky="ew")

        # Frames
        self.home_frame = HomeFrame(self, self.db_manager)
        self.register_frame = RegisterFrame(self, self.face_recognizer)
        self.attendance_frame = AttendanceFrame(self, self.face_recognizer)

        # Select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.register_button.configure(fg_color=("gray75", "gray25") if name == "register" else "transparent")
        self.attendance_button.configure(fg_color=("gray75", "gray25") if name == "attendance" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.home_frame.update_stats() # Refresh stats
        else:
            self.home_frame.grid_forget()
            
        if name == "register":
            self.register_frame.grid(row=0, column=1, sticky="nsew")
            self.register_frame.start_camera()
        else:
            self.register_frame.grid_forget()
            self.register_frame.stop_camera()

        if name == "attendance":
            self.attendance_frame.grid(row=0, column=1, sticky="nsew")
            self.attendance_frame.start_camera()
        else:
            self.attendance_frame.grid_forget()
            self.attendance_frame.stop_camera()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def register_button_event(self):
        self.select_frame_by_name("register")

    def attendance_button_event(self):
        self.select_frame_by_name("attendance")
