#!/usr/bin/env python3
"""
Mac Discord Rich Presence Tracker
A minimal application that tracks active Mac applications and updates Discord status.
"""

import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import os
import logging
from pypresence import Presence

# Configure logging (console only)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MacWindowMonitor:
    """Monitor active window on macOS using AppleScript"""
    
    def get_active_app(self):
        """Get the currently active application name"""
        try:
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
                return frontApp
            end tell
            '''
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            logger.error(f"Error getting active app: {e}")
        return None

class DiscordRPCManager:
    """Manage Discord Rich Presence connection and updates"""
    
    def __init__(self, client_id="1404326169888690296"):
        self.client_id = client_id
        self.rpc = None
        self.connected = False
    
    def connect(self):
        """Connect to Discord RPC"""
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            logger.info("Connected to Discord RPC")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Discord: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from Discord RPC"""
        if self.rpc and self.connected:
            try:
                self.rpc.close()
                self.connected = False
                logger.info("Disconnected from Discord RPC")
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")
    
    def update_status(self, app_name, custom_message=""):
        """Update Discord status with current app"""
        if not self.connected or not self.rpc:
            return False
        
        try:
            display_name = self.get_display_name(app_name)
            details = f"Using {display_name}"
            if custom_message:
                details = f"{custom_message} - {display_name}"
            
            self.rpc.update(
                details=details,
                state="Active",
                start=int(time.time())
            )
            return True
        except Exception as e:
            logger.error(f"Failed to update status: {e}")
            return False
    
    def get_display_name(self, app_name):
        """Get display name for app (simple cleanup)"""
        if not app_name:
            return "Unknown App"
        
        # Basic cleanup - remove common suffixes and clean up name
        name = app_name.replace(".app", "").strip()
        return name if name else "Unknown App"

class WhatIsBroDoingGUI:
    """Main GUI application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("What Is Bro Doing - Mac Discord Tracker")
        self.root.geometry("500x600")
        
        # Initialize components
        self.monitor = MacWindowMonitor()
        self.discord_rpc = DiscordRPCManager()
        
        # State variables
        self.tracking = False
        self.current_app = "None"
        self.tracking_thread = None
        
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Configure root window styling
        self.root.configure(bg="#2b2b2b")
        
        # Title
        title_label = tk.Label(self.root, text="Mac Discord Rich Presence Tracker", 
                              font=("Arial", 18, "bold"), bg="#2b2b2b", fg="#ffffff")
        title_label.grid(row=0, column=0, columnspan=2, pady=15)
        
        # Connection status
        self.connection_label = tk.Label(self.root, text="Discord: Disconnected", 
                                        fg="#ff6b6b", bg="#2b2b2b", font=("Arial", 11))
        self.connection_label.grid(row=1, column=0, columnspan=2, pady=8)
        
        # Status info frame
        info_frame = tk.Frame(self.root, bg="#3c3c3c", relief="ridge", bd=1)
        info_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        # Current app
        tk.Label(info_frame, text="Current App:", bg="#3c3c3c", fg="#cccccc", 
                font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=15, pady=8)
        self.app_label = tk.Label(info_frame, text="None", font=("Arial", 10, "bold"), 
                                 bg="#3c3c3c", fg="#4ecdc4")
        self.app_label.grid(row=0, column=1, sticky="w", pady=8)
        
        # Tracking status
        tk.Label(info_frame, text="Status:", bg="#3c3c3c", fg="#cccccc", 
                font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=15, pady=8)
        self.status_label = tk.Label(info_frame, text="Stopped", fg="#ff6b6b", 
                                    bg="#3c3c3c", font=("Arial", 10, "bold"))
        self.status_label.grid(row=1, column=1, sticky="w", pady=8)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg="#2b2b2b")
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        self.connect_btn = tk.Button(button_frame, text="Connect to Discord", 
                                    command=self.connect_discord, bg="#003D82", fg="white",
                                    font=("Arial", 11, "bold"), relief="flat", padx=25, pady=10,
                                    activebackground="#002A5C", cursor="hand2", bd=0,
                                    highlightthickness=0, disabledforeground="white")
        self.connect_btn.pack(side=tk.LEFT, padx=10)
        
        self.toggle_btn = tk.Button(button_frame, text="Start Tracking", 
                                   command=self.toggle_tracking, bg="#1E7E34", fg="white",
                                   font=("Arial", 11, "bold"), relief="flat", padx=25, pady=10,
                                   activebackground="#155724", cursor="hand2", bd=0,
                                   highlightthickness=0, disabledforeground="white")
        self.toggle_btn.pack(side=tk.LEFT, padx=10)
        
        # Custom message
        message_frame = tk.Frame(self.root, bg="#2b2b2b")
        message_frame.grid(row=4, column=0, columnspan=2, pady=15, padx=20, sticky="ew")
        
        tk.Label(message_frame, text="Custom Message:", bg="#2b2b2b", fg="#cccccc", 
                font=("Arial", 10)).pack(anchor="w")
        self.message_entry = tk.Entry(message_frame, width=50, bg="#3c3c3c", fg="#ffffff", 
                                     font=("Arial", 10), relief="flat", bd=5)
        self.message_entry.pack(fill="x", pady=(5, 0))
        
        # Log area
        log_frame = tk.Frame(self.root, bg="#2b2b2b")
        log_frame.grid(row=5, column=0, columnspan=2, pady=15, padx=20, sticky="nsew")
        
        tk.Label(log_frame, text="Activity Log:", bg="#2b2b2b", fg="#cccccc", 
                font=("Arial", 10)).pack(anchor="w")
        
        # Create text widget without scrollbar
        self.log_text = tk.Text(log_frame, height=12, width=60, bg="#1e1e1e", fg="#ffffff", 
                               font=("Consolas", 9), relief="flat", bd=5, state="disabled",
                               wrap="word")
        self.log_text.pack(fill="both", expand=True, pady=(5, 0))
        
        # Configure grid weights
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
    
    def log_message(self, message):
        """Add message to log area"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Temporarily enable text widget to insert message
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")  # Make it read-only again
        
        logger.info(message)
    
    def connect_discord(self):
        """Connect to Discord"""
        if self.discord_rpc.connect():
            self.connection_label.config(text="Discord: Connected", fg="#57f287")
            self.connect_btn.config(text="Disconnect", command=self.disconnect_discord, bg="#FF3B30", activebackground="#D70015")
            self.log_message("Connected to Discord successfully")
        else:
            self.log_message("Failed to connect to Discord")
    
    def disconnect_discord(self):
        """Disconnect from Discord"""
        self.discord_rpc.disconnect()
        self.connection_label.config(text="Discord: Disconnected", fg="#ff6b6b")
        self.connect_btn.config(text="Connect to Discord", command=self.connect_discord, bg="#003D82", activebackground="#002A5C")
        self.log_message("Disconnected from Discord")
    
    def toggle_tracking(self):
        """Toggle tracking on/off"""
        if self.tracking:
            self.stop_tracking()
        else:
            self.start_tracking()
    
    def start_tracking(self):
        """Start tracking active applications"""
        if not self.discord_rpc.connected:
            self.log_message("Please connect to Discord first")
            return
        
        self.tracking = True
        self.status_label.config(text="Running", fg="#57f287")
        self.toggle_btn.config(text="Stop Tracking", bg="#FF3B30", activebackground="#D70015")
        
        self.tracking_thread = threading.Thread(target=self.tracking_loop, daemon=True)
        self.tracking_thread.start()
        
        self.log_message("Started tracking applications")
    
    def stop_tracking(self):
        """Stop tracking applications"""
        self.tracking = False
        self.status_label.config(text="Stopped", fg="#ff6b6b")
        self.toggle_btn.config(text="Start Tracking", bg="#1E7E34", activebackground="#155724")
        self.log_message("Stopped tracking applications")
    
    def tracking_loop(self):
        """Main tracking loop"""
        last_app = None
        
        while self.tracking:
            try:
                current_app = self.monitor.get_active_app()
                
                if current_app and current_app != last_app:
                    self.current_app = current_app
                    self.app_label.config(text=current_app)
                    
                    custom_message = self.message_entry.get().strip()
                    if self.discord_rpc.update_status(current_app, custom_message):
                        self.log_message(f"Updated status: {current_app}")
                    
                    last_app = current_app
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                self.log_message(f"Error in tracking loop: {e}")
                time.sleep(5)
    
    def on_closing(self):
        """Handle window closing"""
        self.tracking = False
        if self.discord_rpc.connected:
            self.discord_rpc.disconnect()
        self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.log_message("Mac Discord Tracker started")
        self.root.mainloop()

def main():
    """Main entry point"""
    # Start the application
    app = WhatIsBroDoingGUI()
    app.run()

if __name__ == "__main__":
    main()
