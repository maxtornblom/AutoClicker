import time
import threading
import json
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key

# Global variables to store delay and button settings
settings_lock = threading.Lock()  # Thread-safe lock for shared variables
delay = 0.01
button = Button.left


# Load settings from JSON file
def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            return settings["delay"], settings["button"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        print("Error loading settings, using default values.")
        return 0.01, "left"


# Update settings dynamically
def update_settings():
    global delay, button
    while True:
        new_delay, new_button_str = load_settings()

        # Convert button string to pynput Button object
        new_button = Button.left if new_button_str == "left" else Button.right

        # Update settings safely using the lock
        with settings_lock:
            delay = new_delay
            button = new_button

        time.sleep(1)  # Check for updates every second


# Thread for managing mouse clicks
class ClickMouse(threading.Thread):
    def __init__(self):
        super(ClickMouse, self).__init__()
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                with settings_lock:  # Safely access shared settings
                    current_delay = delay
                    current_button = button

                mouse.click(current_button)
                time.sleep(current_delay)
            time.sleep(0.1)


# Instance of mouse controller is created
mouse = Controller()
click_thread = ClickMouse()
click_thread.start()


# Function to handle key press events
def on_press(key):
    if key == Key.caps_lock:  # Start/stop clicking with 'a'
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == KeyCode(char="q"):  # Quit with 'q'
        click_thread.exit()
        listener.stop()


# Start listener for keyboard input
listener = Listener(on_press=on_press)
listener.start()

# Start settings update thread
settings_thread = threading.Thread(target=update_settings)
settings_thread.daemon = True  # Ensure the settings thread exits with the program
settings_thread.start()

# Join the listener to wait for key events
listener.join()
