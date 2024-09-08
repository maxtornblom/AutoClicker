import tkinter as tk
from tkinter import ttk
import json  # Import JSON module for saving the settings


# Function to update the delay and button based on UI input
def update_settings():
    try:
        # Update delay and button settings
        current_delay = float(delay_display.get())
        selected_button = (
            button.get().lower()
        )  # Convert button to lowercase for consistency

        # Create a dictionary to store the settings
        settings = {"delay": current_delay, "button": selected_button}

        # Save the settings to a JSON file
        with open("settings.json", "w") as f:
            json.dump(
                settings, f, indent=4
            )  # Save the dictionary to a JSON file with indentation for readability

        print(f"Updated delay: {current_delay}, button: {selected_button}")

    except ValueError:
        print("Invalid input for delay")


# Creating the tkinter UI
root = tk.Tk()
root.title("Auto Clicker Settings")

# Delay setting
delay_display = tk.StringVar(value="0.1")
ttk.Label(root, text="Delay (seconds):").grid(row=0, column=0, padx=10, pady=10)
ttk.Entry(root, textvariable=delay_display).grid(row=0, column=1, padx=10, pady=10)

# Button setting
button = tk.StringVar(value="Right")
ttk.Label(root, text="Button:").grid(row=1, column=0, padx=10, pady=10)
button_menu = ttk.OptionMenu(root, button, "Left", "Left", "Right")
button_menu.grid(row=1, column=1, padx=10, pady=10)

# Update button
ttk.Button(root, text="Update Settings", command=update_settings).grid(
    row=2, column=0, columnspan=2, padx=10, pady=10
)

# Start the tkinter main loop
root.mainloop()
