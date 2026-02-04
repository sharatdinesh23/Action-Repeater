import time, json, subprocess, pyautogui
from pathlib import Path

BASE = Path(__file__).parent
WF = BASE / "workflow.json"

from pynput.keyboard import Key
import pyautogui

pyautogui.FAILSAFE = False


KEY_MAP = {
    "Key.enter": "enter",
    "Key.space": "space",
    "Key.backspace": "backspace",
    "Key.tab": "tab",
    "Key.esc": "esc",
    "Key.up": "up",
    "Key.down": "down",
    "Key.left": "left",
    "Key.right": "right"
}



def find(anchor):
    for c in (0.8, 0.7, 0.6):
        try:
            loc = pyautogui.locateOnScreen(anchor, confidence=c, grayscale=True)
            if loc:
                return loc
        except:
            pass
    return None


def execute():
    with open(WF) as f:
        steps = json.load(f)

    for step in steps:
        time.sleep(step.get("delay", 0))

        if step["action"] == "start_app":
            subprocess.Popen(step["command"], shell=True)
            time.sleep(2)

        elif step["action"] == "click":
            loc = find(step["anchor"])
            if loc:
                pyautogui.click(
                    loc.left + loc.width // 2,
                    loc.top + loc.height // 2
                )
            else:
                print("⚠ click skipped")

        elif step["action"] == "key":
            key_name = KEY_MAP.get(step["key"])
            if key_name:
                pyautogui.press(key_name)


        elif step["action"] == "type":
            pyautogui.write(step["value"])

    print("✓ Execution finished")


if __name__ == "__main__":
    execute()
