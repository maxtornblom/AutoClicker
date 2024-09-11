import customtkinter as ctk
import json
import os
import threading

file_lock = threading.Lock()
root = None  # Global variable for the GUI root window

def show_warning(message):
    warning_popup = ctk.CTkToplevel(root)
    warning_popup.title("Warning")
    warning_popup.geometry("300x100")
    warning_label = ctk.CTkLabel(warning_popup, text=message, padx=20, pady=20)
    warning_label.pack()
    ok_button = ctk.CTkButton(warning_popup, text="OK", command=warning_popup.destroy)
    ok_button.pack()

def update_settings():
    try:
        cps = float(delay_entry.get())
        if cps <= 0:
            show_warning("CPS must be a positive number.")
            return

        # Convert CPS to delay (seconds per click)
        current_delay = 1 / cps
        
        selected_button = button_var.get().lower()
        if selected_button not in ["left", "right"]:
            show_warning("Invalid button selection.")
            return

        settings = {"delay": current_delay, "button": selected_button}

        with file_lock:
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)
    except ValueError:
        show_warning("Please enter a valid number for CPS.")

def load_settings():
    global delay_entry, button_var
    if os.path.exists("settings.json"):
        try:
            with file_lock:
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                    delay_entry.delete(0, ctk.END)
                    # Convert delay back to CPS
                    cps = 1 / settings.get("delay", 0.1)
                    cps = int(round(1 / settings.get("delay", 0.1)))
                    delay_entry.insert(0, str(round(cps, 2)))
                    button_var.set(settings.get("button", "Right").capitalize())
        except json.JSONDecodeError:
            pass

# Function to launch the GUI
def launch_gui(quit_program_callback):
    global delay_entry, button_var, root

    # Initialize the main window
    global root
    root = ctk.CTk()
    root.title("Auto Clicker Settings")
    root.geometry("400x250")
    root.resizable(False, False)

    # Bind the window close event to quit the entire program
    root.protocol("WM_DELETE_WINDOW", quit_program_callback)

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    cps_label = ctk.CTkLabel(root, text="CPS (clicks per second):")
    cps_label.grid(row=0, column=0, padx=(30, 10), pady=(30, 10), sticky="e")

    delay_entry = ctk.CTkEntry(root, placeholder_text="Enter CPS", width=200)
    delay_entry.grid(row=0, column=1, padx=(10, 30), pady=(30, 10), sticky="w")

    button_label = ctk.CTkLabel(root, text="Button:")
    button_label.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="e")

    button_var = ctk.StringVar(value="Right")
    button_menu = ctk.CTkOptionMenu(root, variable=button_var, values=["Left", "Right"], width=200)
    button_menu.grid(row=1, column=1, padx=(10, 30), pady=10, sticky="w")

    update_button = ctk.CTkButton(root, text="Update Settings", command=update_settings, width=200)
    update_button.grid(row=2, column=0, columnspan=2, padx=30, pady=(20, 10))

    load_settings()

    root.mainloop()

def quit_gui():
    global root
    if root is not None:
        try:
            root.quit()  # Stop the main loop
            root.destroy()  # Close the GUI window
        except Exception as e:
            print(f"Error while destroying the GUI: {e}")
