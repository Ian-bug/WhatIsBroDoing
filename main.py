"""
MIT License
Copyright (c) 2024 Ian-bug
See LICENSE file for details.
"""

import time
from pypresence import Presence
import pygetwindow as gw
import psutil
import win32process
import win32gui
from applist import app_names  # 導入應用程式對照表
import os
import signal
import sys 
import logging

    
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log")),
        logging.StreamHandler()
    ]
)

def signal_handler(sig, frame):
    print("\n Exiting What Is Bro Doing")
    RPC.close
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

start_opinion = input("start or edit applist? (0/1): ")
if start_opinion == "1":
    if os.path.exists("applist.py"):
        with open("applist.py", "r", encoding="utf-8") as f:
            current_list = f.read()
        print("Current applist content:")
        print(current_list)
        
        process_name = input("Enter process name (example: chrome.exe): ")
        if not process_name:
            print("No process name entered. Exiting.")
            exit()
            
        # Check if process name already exists
        if f"'{process_name}'" in current_list:
            override = input("This process already exists. Override? (y/n): ")
            if override.lower() != 'y':
                print("Operation cancelled.")
            exit()
        
        display_name = input("Enter display name (example: Google Chrome): ")
        if not display_name:
            print("No display name entered. Exiting.")
            exit()
            
        new_app = f"'{process_name}': '{display_name}'"
        
        if f"'{process_name}'" in current_list:
            # 替換現有項目
            with open("applist.py", "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            with open("applist.py", "w", encoding="utf-8") as f:
                found = False
                for line in lines:
                    if f"'{process_name}'" in line:
                        # 跳過舊的項目
                        continue
                    if "}" in line and not found:
                        # 在字典結束前添加新項目
                        f.write(f"    {new_app},\n")
                        found = True
                    f.write(line)
        else:
            # 添加新項目
            with open("applist.py", "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            with open("applist.py", "w", encoding="utf-8") as f:
                for i, line in enumerate(lines):
                    if "}" in line:
                        # 在字典結束前添加新項目
                        f.write(f"    {new_app},\n")
                        f.write(line)
                    else:
                        f.write(line)

        print("Updated applist.py")
        exit()
    else:
        print("applist.py not found")
        exit()

client_id = "1404326169888690296"

RPC = Presence(client_id)
RPC.connect()

start_time = int(time.time())  # 啟動時記錄
RPC.update(buttons=[{"label": "Get What Is Bro Doing", "url": "https://github.com/Ian-bug/WhatIsBroDoing"}]) 
# https://qwertyquerty.github.io/pypresence/html/doc/presence.html :nerd:

last_procname = None

details_input = input("type details you want (if empty, defaults to 'bro is doing'): ")
if details_input == "":
    details = "bro is doing"
else:
    details = details_input

while True:
    try:
        win = gw.getActiveWindow()
        if win:
            hwnd = win._hWnd
            tid, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid)
            procname = proc.name()
            # 檢查程式是否在對照表中，如果在則使用對應的名稱
            display_name = app_names.get(procname, procname)
        else:
            procname = "unknown"
            display_name = procname
            pid = None
        if procname != last_procname:
            print("switching to:", display_name)
            buttons = [{"label": "Get What Is Bro Doing", "url": "https://github.com/Ian-bug/WhatIsBroDoing"}]
            if pid is not None and isinstance(pid, int):
                RPC.update(details=details + ": ", state=display_name, pid=pid, start=start_time, buttons=buttons)
            else:
                RPC.update(details=details + ": ", state=display_name, start=start_time, buttons=buttons)
            last_procname = procname
    except Exception as e:
        print(e)
    time.sleep(1)