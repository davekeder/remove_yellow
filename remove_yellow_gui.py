import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox



# --- Updated Yellow Removal ---
def remove_yellow_highlights(input_dir, output_dir, log_callback, grayscale_output):
    os.makedirs(output_dir, exist_ok=True)
    count = 0

    # --- Yellow color HSV range ---
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])


    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        img = cv2.imread(input_path)
        if img is None:
            log_callback(f"⚠️ Skipped: {filename} (unreadable)")
            continue

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        img[mask != 0] = [255, 255, 255]

        if grayscale_output:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imwrite(output_path, img)
        log_callback(f"✅ Saved: {filename}")
        count += 1

    messagebox.showinfo("Done", f"Finished processing {count} image(s).")



# --- Updated GUI class ---
class YellowRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yellow Highlight Remover")
        self.root.geometry("500x340")

        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.grayscale_var = tk.BooleanVar(value=False)

        tk.Label(root, text="Input Folder:").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(root, textvariable=self.input_dir, width=60).pack(padx=10)
        tk.Button(root, text="Browse", command=self.browse_input).pack(pady=(0, 10))

        tk.Label(root, text="Output Folder:").pack(anchor="w", padx=10)
        tk.Entry(root, textvariable=self.output_dir, width=60).pack(padx=10)
        tk.Button(root, text="Browse", command=self.browse_output).pack(pady=(0, 10))

        tk.Checkbutton(root, text="Output in grayscale", variable=self.grayscale_var).pack()

        tk.Button(root, text="Run", command=self.run).pack(pady=10)

        self.log = tk.Text(root, height=8, width=60, state="disabled")
        self.log.pack(padx=10, pady=10)

    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_dir.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def log_message(self, msg):
        self.log.config(state="normal")
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state="disabled")

    def run(self):
        in_dir = self.input_dir.get()
        out_dir = self.output_dir.get()

        if not os.path.isdir(in_dir) or not os.path.isdir(out_dir):
            messagebox.showerror("Error", "Please select valid input and output folders.")
            return

        self.log_message("Starting...")
        self.root.update_idletasks()

        remove_yellow_highlights(
            in_dir,
            out_dir,
            self.log_message,
            grayscale_output=self.grayscale_var.get()
        )

        self.log_message("Done.")



# --- Launch ---
if __name__ == "__main__":
    root = tk.Tk()
    app = YellowRemoverApp(root)
    root.mainloop()