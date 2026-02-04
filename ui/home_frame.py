import customtkinter as ctk

class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db = db_manager
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Log list expands

        self.label = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Stats
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid(row=1, column=0, padx=20, pady=0, sticky="ew")
        
        # Logs Title
        self.logs_label = ctk.CTkLabel(self, text="Recent Activity", font=ctk.CTkFont(size=18, weight="bold"))
        self.logs_label.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Logs List (Scrollable)
        self.logs_frame = ctk.CTkScrollableFrame(self)
        self.logs_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        
        self.refresh_button = ctk.CTkButton(self, text="Refresh Data", command=self.update_stats)
        self.refresh_button.grid(row=4, column=0, padx=20, pady=20, sticky="e")
        
        self.update_stats()

    def update_stats(self):
        # Stats
        stats = self.db.get_stats()
        
        # Clear previous widgets in stats frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        stat_label_users = ctk.CTkLabel(self.stats_frame, text=f"Total Registered Users: {stats['users']}", 
                                  font=ctk.CTkFont(size=18))
        stat_label_users.pack(pady=5, padx=20)
        
        stat_label_today = ctk.CTkLabel(self.stats_frame, text=f"Today's Attendance: {stats['today']}", 
                                  font=ctk.CTkFont(size=18))
        stat_label_today.pack(pady=5, padx=20)
        
        # Recent Logs
        # Clear previous logs
        for widget in self.logs_frame.winfo_children():
            widget.destroy()
            
        logs = self.db.get_recent_logs(limit=20)
        
        if not logs:
            no_log_label = ctk.CTkLabel(self.logs_frame, text="No recent activity.")
            no_log_label.pack(pady=10)
        else:
            # Header
            header_frame = ctk.CTkFrame(self.logs_frame, fg_color="transparent")
            header_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(header_frame, text="Name", font=ctk.CTkFont(weight="bold"), width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Time", font=ctk.CTkFont(weight="bold"), width=150, anchor="w").pack(side="left", padx=5)

            for log in logs:
                # log is a tuple: (name, timestamp)
                name, timestamp = log
                
                row_frame = ctk.CTkFrame(self.logs_frame)
                row_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(row_frame, text=name, width=150, anchor="w").pack(side="left", padx=5)
                ctk.CTkLabel(row_frame, text=str(timestamp), width=150, anchor="w").pack(side="left", padx=5)
