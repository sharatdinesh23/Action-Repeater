import tkinter as tk, subprocess, sys
from pathlib import Path

BASE = Path(__file__).parent

def run(f):
    subprocess.Popen([sys.executable, str(BASE / f)])

root = tk.Tk()
root.title("Python RPA Studio")
root.geometry("300x200")

tk.Button(root, text="▶ Start Recording",
          command=lambda: run("recorder.py"), height=2).pack(pady=10)

tk.Label(root, text="Press ESC to stop").pack()

tk.Button(root, text="▶ Play Workflow",
          command=lambda: run("executor.py"), height=2).pack(pady=10)

root.mainloop()
