Yellow Highlight Remover
=========================

This is a simple desktop application that removes yellow highlights from screenshots or scanned documents. It's especially useful for cleaning up study materials (e.g., PDFs or image sets) where yellow was used to mark correct answers.

Features:
---------
- Removes yellow highlighting from PNG, JPG, and JPEG images
- Optional checkbox to output in grayscale instead of color
- User-friendly GUI with folder selection and live progress log
- Built with Python, OpenCV, and Tkinter
- Can be packaged as a standalone Windows .exe (no Python required)

How to Use:
-----------
1. Open the app (double-click `remove_yellow_gui.exe`)
2. Select the input folder (contains your original screenshots)
3. Select the output folder (where cleaned images will be saved)
4. Check "Output in grayscale" if you want black & white images
5. Click "Run" to process all supported image files

Usage Notes:
------------
- Highlight removal works best on clean, well-lit screenshots.
- Grayscale output may improve clarity when yellow is too blended to isolate.
- Unsupported or unreadable image files are automatically skipped.

Building the App:
-----------------
To build the `.exe`:
    pip install pyinstaller
    pyinstaller --noconsole --onefile remove_yellow_gui.py

Dependencies:
-------------
- Python 3.7+
- opencv-python
- tkinter (included in standard Python distributions)

Repository Files:
-----------------
- remove_yellow_gui.py         # Main application script
- README.txt                   # Project description
- (optional) icon.ico          # App icon for Windows builds
- (optional) /dist             # Where the executable is placed after building

License:
--------
MIT License or custom — feel free to adapt and improve.

