import time
import json
import pyautogui
from pynput import mouse, keyboard
from pathlib import Path

BASE_DIR = Path(__file__).parent
ANCHOR_DIR = BASE_DIR / "anchors"
ANCHOR_DIR.mkdir(exist_ok=True)

actions = []
last_time = time.time()
recording = True


def dt():
    global last_time
    now = time.time()
    d = round(now - last_time, 3)
    last_time = now
    return d


def capture_anchor(x, y):
    img = pyautogui.screenshot(region=(x - 80, y - 80, 160, 160))
    path = ANCHOR_DIR / f"anchor_{len(actions)}.png"
    img.save(path)
    return str(path)


def on_click(x, y, button, pressed):
    if not recording or not pressed:
        return

    anchor = capture_anchor(x, y)

    actions.append({
        "action": "click",
        "anchor": anchor,
        "delay": dt()
    })


def on_press(key):
    if not recording:
        return

    try:
        value = key.char
    except:
        return

    actions.append({
        "action": "type",
        "value": value,
        "delay": dt()
    })


def on_release(key):
    global recording
    if key == keyboard.Key.esc:
        recording = False
        return False


print("● Recording started (ESC to stop)")

mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()
mouse_listener.stop()

workflow = BASE_DIR / "workflow.json"
with open(workflow, "w", encoding="utf-8") as f:
    json.dump(actions, f, indent=2)

print(f"✓ Workflow saved → {workflow}")
