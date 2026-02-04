import time, json, pyautogui
from pynput import mouse, keyboard
from pathlib import Path

BASE = Path(__file__).parent
ANCHORS = BASE / "anchors"
ANCHORS.mkdir(exist_ok=True)

actions = []
last = time.time()
recording = True


def dt():
    global last
    now = time.time()
    d = round(now - last, 3)
    last = now
    return d


def capture(x, y):
    img = pyautogui.screenshot(region=(x - 80, y - 80, 160, 160))
    path = ANCHORS / f"anchor_{len(actions)}.png"
    img.save(path)
    return str(path)


def on_click(x, y, button, pressed):
    if not recording or not pressed:
        return

    actions.append({
        "action": "click",
        "anchor": capture(x, y),
        "delay": dt()
    })


from pynput.keyboard import Key

def on_press(key):
    if not recording:
        return

    delay = dt()

    if isinstance(key, Key):
        actions.append({
            "action": "key",
            "key": str(key),   # e.g. Key.enter
            "delay": delay
        })
    else:
        actions.append({
            "action": "type",
            "value": key.char,
            "delay": delay
        })



def on_release(key):
    global recording
    if key == keyboard.Key.esc:
        recording = False
        return False


print("● Recording started (ESC to stop)")
ml = mouse.Listener(on_click=on_click)
kl = keyboard.Listener(on_press=on_press, on_release=on_release)
ml.start()
kl.start()
kl.join()
ml.stop()

with open(BASE / "workflow.json", "w") as f:
    json.dump(actions, f, indent=2)

print("✓ workflow.json saved")
