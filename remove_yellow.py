import cv2
import numpy as np
import os

# --- CONFIGURATION ---
input_folder = "screenshots"     # Folder containing original screenshots
output_folder = "processed"      # Folder to save processed images
os.makedirs(output_folder, exist_ok=True)

# --- HSV Yellow Color Range (tweak if needed) ---
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([40, 255, 255])

# --- Supported image formats ---
supported_exts = ('.png', '.jpg', '.jpeg')

# --- Process each image ---
for filename in os.listdir(input_folder):
    if filename.lower().endswith(supported_exts):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Read and convert image
        img = cv2.imread(input_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Create mask for yellow pixels
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Replace yellow pixels with white (or black or transparent)
        img[mask != 0] = [255, 255, 255]

        # Save result
        cv2.imwrite(output_path, img)

        print(f"Processed: {filename}")
