import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps


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

def generate_pdf_native_images(input_dir, output_dir, log_callback):
    import os
    import tempfile
    from PIL import Image
    from reportlab.pdfgen import canvas

    def build_pdf(images, pdf_path, label):
        try:
            c = canvas.Canvas(pdf_path)
            temp_files = []

            for img in images:
                w, h = img.size
                margin = h // 2
                page_width = w
                page_height = h + 2 * margin
                c.setPageSize((page_width, page_height))

                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False, dir=output_dir) as tmp:
                    temp_path = tmp.name
                    img.save(temp_path, "JPEG")
                    temp_files.append(temp_path)

                c.drawImage(temp_path, 0, margin, width=w, height=h)
                c.showPage()

            c.save()

            for temp_path in temp_files:
                try:
                    os.remove(temp_path)
                except:
                    pass

            log_callback(f"📄 {label} PDF saved: {pdf_path}")
        except Exception as e:
            log_callback(f"⚠️ Failed to generate {label} PDF: {str(e)}")

    # Load processed images
    processed_images = []
    for filename in sorted(os.listdir(output_dir)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(os.path.join(output_dir, filename)).convert("RGB")
                processed_images.append(img)
            except:
                log_callback(f"⚠️ Skipped unreadable processed image: {filename}")

    if processed_images:
        build_pdf(processed_images, os.path.join(output_dir, "output.pdf"), "Processed")
    else:
        log_callback("⚠️ No processed images found.")

    # Load original images
    original_images = []
    for filename in sorted(os.listdir(input_dir)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(os.path.join(input_dir, filename)).convert("RGB")
                original_images.append(img)
            except:
                log_callback(f"⚠️ Skipped unreadable original image: {filename}")

    if original_images:
        build_pdf(original_images, os.path.join(output_dir, "originals.pdf"), "Original")
    else:
        log_callback("⚠️ No original images found.")


# --- Updated GUI class ---
class YellowRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yellow Highlight Remover")
        self.root.geometry("500x340")

        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.grayscale_var = tk.BooleanVar(value=False)
        self.pdf_var = tk.BooleanVar(value=False)
        
        tk.Label(root, text="Input Folder:").pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(root, textvariable=self.input_dir, width=60).pack(padx=10)
        tk.Button(root, text="Browse", command=self.browse_input).pack(pady=(0, 10))

        tk.Label(root, text="Output Folder:").pack(anchor="w", padx=10)
        tk.Entry(root, textvariable=self.output_dir, width=60).pack(padx=10)
        tk.Button(root, text="Browse", command=self.browse_output).pack(pady=(0, 10))

        tk.Checkbutton(root, text="Output in grayscale", variable=self.grayscale_var).pack()
        tk.Checkbutton(root, text="Generate PDF from processed images", variable=self.pdf_var).pack()
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
        
        if self.pdf_var.get():
            self.log_message("Generating PDF...")
            generate_pdf_native_images(in_dir, out_dir, self.log_message)
        
# --- Launch ---
if __name__ == "__main__":
    root = tk.Tk()
    app = YellowRemoverApp(root)
    root.mainloop()