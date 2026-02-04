import time
import json
import pyautogui
from pathlib import Path

BASE_DIR = Path(__file__).parent
WORKFLOW = BASE_DIR / "workflow.json"


def find(anchor):
    for conf in (0.8, 0.7, 0.6):
        try:
            loc = pyautogui.locateOnScreen(
                anchor,
                confidence=conf,
                grayscale=True
            )
            if loc:
                return loc
        except:
            pass
    return None


def execute():
    if not WORKFLOW.exists():
        print("✗ workflow.json not found")
        return

    with open(WORKFLOW, encoding="utf-8") as f:
        steps = json.load(f)

    for step in steps:
        time.sleep(step.get("delay", 0))

        if step["action"] == "click":
            loc = find(step["anchor"])
            if loc:
                x = loc.left + loc.width // 2
                y = loc.top + loc.height // 2
                pyautogui.click(x, y)
                print("✓ Click")
            else:
                print("⚠ Element not found, skipped")

        elif step["action"] == "type":
            pyautogui.write(step["value"])
            print(f"✓ Typed {step['value']}")

    print("✓ Execution complete")


if __name__ == "__main__":
    execute()
