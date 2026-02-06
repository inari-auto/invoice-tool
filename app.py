import tkinter as tk
import subprocess

def run():
    subprocess.run(["python3", "main.py"])

root = tk.Tk()
root.title("請求書自動作成ツール")

btn = tk.Button(
    root,
    text="請求書を作成する",
    width=25,
    height=3,
    command=run
)

btn.pack(padx=40, pady=40)

root.mainloop()