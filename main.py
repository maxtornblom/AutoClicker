import sys
import time
import threading
import json
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key
from gui import launch_gui, quit_gui  # Import the function to launch the GUI

settings_lock = threading.Lock()
delay = 0.01
button = Button.left
file_lock = threading.Lock()

mouse = Controller()

# Flag to indicate if the program should quit
should_quit = threading.Event()

# Load settings from JSON file
def load_settings():
    try:
        with file_lock:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                return settings.get('delay', 0.01), settings.get('button', 'left')
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        print("Error loading settings, using default values.")
        return 0.01, 'left'

def update_settings():
    global delay, button
    while not should_quit.is_set():
        new_delay, new_button_str = load_settings()
        new_button = Button.left if new_button_str == 'left' else Button.right
        with settings_lock:
            delay = new_delay
            button = new_button
        time.sleep(1)

class ClickMouse(threading.Thread):
    def __init__(self):
        super(ClickMouse, self).__init__()
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True
        print("Start clicking")

    def stop_clicking(self):
        self.running = False
        print("Stop clicking")

    def exit(self):
        self.stop_clicking()
        self.program_running = False
        print("Exit auto-clicker")

    def run(self):
        while self.program_running:
            while self.running:
                with settings_lock:
                    current_delay = delay
                    current_button = button
                mouse.click(current_button)
                time.sleep(current_delay)
            time.sleep(0.1)

def on_press(key):
    if key == Key.caps_lock:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == KeyCode(char="q"):
        quit_program()

def quit_program():
    should_quit.set()  # Signal the program to quit
    click_thread.exit()  # Stop the click thread
    listener.stop()  # Stop the keyboard listener
    quit_gui()  # Close the GUI window


# Function to run the auto-clicker and GUI simultaneously
def run_program():
    global click_thread, gui_thread, listener
    click_thread = ClickMouse()
    click_thread.start()

    # Start the keyboard listener
    listener = Listener(on_press=on_press)
    listener.start()

    # Start the settings update thread
    settings_thread = threading.Thread(target=update_settings)
    settings_thread.daemon = True
    settings_thread.start()

    # Run the GUI in a separate thread
    gui_thread = threading.Thread(target=launch_gui, args=(quit_program,))
    gui_thread.start()

    print("Auto-clicker running, press 'Caps Lock' to start/stop, 'q' to quit.")
    should_quit.wait()  # Wait until should_quit is set

    gui_thread.join()  # Wait for the GUI thread to finish
    print("Program has fully exited.")

if __name__ == '__main__':
    run_program()
