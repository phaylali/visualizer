import tkinter as tk
from pynput import keyboard, mouse
import threading
import configparser
import os

# --- Configuration Class ---
class Config:
    """
    Loads and holds the configuration from the config.ini file.
    Provides default values if the file or a setting is missing.
    """
    def __init__(self, filename='config.ini'):
        self.config = configparser.ConfigParser()
        # Check if config file exists, if not, it will use defaults
        if os.path.exists(filename):
            self.config.read(filename)
        
        # --- Appearance Settings ---
        self.font_family = self.config.get('Appearance', 'font_family', fallback='Tajawal')
        self.font_size = self.config.getint('Appearance', 'font_size', fallback=24)
        self.text_color = self.config.get('Appearance', 'text_color', fallback='white')
        self.bg_color = self.config.get('Appearance', 'bg_color', fallback='#2E2E2E')
        self.padding_x = self.config.getint('Appearance', 'padding_x', fallback=20)
        self.padding_y = self.config.getint('Appearance', 'padding_y', fallback=10)
        self.duration_ms = self.config.getint('Appearance', 'duration_ms', fallback=1500)
        
        # --- Position Settings ---
        self.position = self.config.get('Position', 'position', fallback='bottom-center')
        self.x_offset = self.config.getint('Position', 'x_offset', fallback=0)
        self.y_offset = self.config.getint('Position', 'y_offset', fallback=-150)


# --- Main Application Class ---
class KeystrokeVisualizer:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.root.withdraw()
        
        self.input_queue = []
        self.queue_lock = threading.Lock()
        
        self.process_queue()

    def calculate_position(self, window):
        """Calculates the (x, y) coordinates for the overlay based on config."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window.update_idletasks()
        win_width = window.winfo_width()
        win_height = window.winfo_height()

        position_map = {
            'top-left': (0, 0),
            'top-center': ((screen_width // 2) - (win_width // 2), 0),
            'top-right': (screen_width - win_width, 0),
            'center': ((screen_width // 2) - (win_width // 2), (screen_height // 2) - (win_height // 2)),
            'bottom-left': (0, screen_height - win_height),
            'bottom-center': ((screen_width // 2) - (win_width // 2), screen_height - win_height),
            'bottom-right': (screen_width - win_width, screen_height - win_height),
        }

        base_x, base_y = position_map.get(self.config.position, position_map['bottom-center'])
        
        # Apply offsets from the config file
        final_x = base_x + self.config.x_offset
        final_y = base_y + self.config.y_offset

        return final_x, final_y

    def display_input(self, input_char):
        input_window = tk.Toplevel(self.root)
        
        input_window.wm_attributes("-topmost", True)
        input_window.overrideredirect(True)
        input_window.config(bg=self.config.bg_color)

        input_label = tk.Label(
            input_window,
            text=input_char,
            font=(self.config.font_family, self.config.font_size, "bold"),
            bg=self.config.bg_color,
            fg=self.config.text_color,
            padx=self.config.padding_x,
            pady=self.config.padding_y
        )
        input_label.pack()

        x_pos, y_pos = self.calculate_position(input_window)
        input_window.geometry(f"+{x_pos}+{y_pos}")

        input_window.after(self.config.duration_ms, input_window.destroy)

    def add_to_queue(self, input_char):
        with self.queue_lock:
            self.input_queue.append(input_char)

    def process_queue(self):
        with self.queue_lock:
            if self.input_queue:
                input_char = self.input_queue.pop(0)
                self.display_input(input_char)
        self.root.after(50, self.process_queue)


# --- Input Listener Logic (largely unchanged) ---
def on_key_press(key, visualizer_app):
    key_char = ''
    try:
        key_char = key.char
        if key_char is None: raise AttributeError
    except AttributeError:
        key_name = str(key).replace('Key.', '')
        if 'cmd' in key_name or 'win' in key_name: key_char = 'Super'
        elif '_' in key_name: key_char = key_name.split('_')[0]
        else: key_char = key_name
    
    special_keys_map = {
        'space': '␣', 'enter': '⏎', 'backspace': '⌫', 'shift': '⇧',
        'ctrl': '⌃', 'alt': '⌥', 'tab': '⇥', 'super': '❖', 'esc': 'Esc',
    }
    
    key_lower = key_char.lower()
    if key_lower in special_keys_map: key_display = special_keys_map[key_lower]
    elif len(key_char) == 1: key_display = key_char.upper()
    else: key_display = key_char.capitalize()

    if key_display: visualizer_app.add_to_queue(key_display)

def on_mouse_click(x, y, button, pressed, visualizer_app):
    if pressed:
        if button == mouse.Button.left: display_char = "LMB"
        elif button == mouse.Button.right: display_char = "RMB"
        elif button == mouse.Button.middle: display_char = "MMB"
        else: display_char = "Mouse"
        visualizer_app.add_to_queue(display_char)

def on_mouse_scroll(x, y, dx, dy, visualizer_app):
    if dy > 0: display_char = "▲"
    elif dy < 0: display_char = "▼"
    else: return
    visualizer_app.add_to_queue(display_char)

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Load configuration first
    config = Config('config.ini')

    # 2. Create the main Tkinter window and our app instance
    root_window = tk.Tk()
    app = KeystrokeVisualizer(root_window, config)
    
    # --- Listener Threads ---
    keyboard_listener = keyboard.Listener(on_press=lambda key: on_key_press(key, app))
    keyboard_thread = threading.Thread(target=keyboard_listener.start, daemon=True)
    keyboard_thread.start()

    mouse_listener = mouse.Listener(
        on_click=lambda x, y, button, pressed: on_mouse_click(x, y, button, pressed, app),
        on_scroll=lambda x, y, dx, dy: on_mouse_scroll(x, y, dx, dy, app)
    )
    mouse_thread = threading.Thread(target=mouse_listener.start, daemon=True)
    mouse_thread.start()

    # 3. Start the main GUI loop
    root_window.mainloop()