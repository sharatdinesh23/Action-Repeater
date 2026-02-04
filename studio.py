import tkinter as tk
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent


def run(script):
    subprocess.Popen([sys.executable, str(BASE_DIR / script)])


root = tk.Tk()
root.title("Python RPA Studio")
root.geometry("300x200")

tk.Button(root, text="▶ Start Recording", height=2,
          command=lambda: run("recorder.py")).pack(pady=10)

tk.Label(root, text="Press ESC to stop recording").pack()

tk.Button(root, text="▶ Play Workflow", height=2,
          command=lambda: run("executor.py")).pack(pady=10)

root.mainloop()
