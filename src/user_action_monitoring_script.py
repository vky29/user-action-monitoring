import psutil
import time
from pynput import mouse, keyboard
from datetime import datetime

# Log file to store user actions
log_file = "user_actions.log"


# Get active window title (only works on Windows)
def get_active_window_title():
    try:
        import win32gui
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except ImportError:
        return "Active window tracking only supported on Windows."


# Log action to file
def log_action(action):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} - {action}\n")


# Mouse event handlers
def on_click(x, y, button, pressed):
    action = f"Mouse {'Pressed' if pressed else 'Released'} at ({x}, {y}) with {button}"
    print(action)
    log_action(action)


def on_move(x, y):
    action = f"Mouse moved to ({x}, {y})"
    print(action)
    log_action(action)


# Keyboard event handlers
def on_press(key):
    try:
        action = f"Key '{key.char}' pressed"
    except AttributeError:
        action = f"Special Key '{key}' pressed"
    print(action)
    log_action(action)


def on_release(key):
    action = f"Key '{key}' released"
    print(action)
    log_action(action)
    if key == keyboard.Key.esc:
        return False  # Stop listener


# Track active window
def track_active_window():
    previous_window = None
    while True:
        current_window = get_active_window_title()
        if current_window != previous_window:
            action = f"Active window changed to: {current_window}"
            print(action)
            log_action(action)
            previous_window = current_window
        time.sleep(1)


# Start tracking
if __name__ == "__main__":
    # Start mouse and keyboard listeners
    with mouse.Listener(on_click=on_click, on_move=on_move) as mouse_listener, \
            keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
        # Run active window tracking in parallel
        import threading

        window_thread = threading.Thread(target=track_active_window)
        window_thread.daemon = True
        window_thread.start()

        # Join listeners to keep the program running
        mouse_listener.join()
        keyboard_listener.join()
