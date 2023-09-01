import cv2
import qrcode
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

# Function to encode text into a QR code
def encode_text():
    text = text_entry.get()
    if text:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("encoded_qr.png")
        show_qr_code("encoded_qr.png")
    else:
        messagebox.showwarning("Warning", "Please enter text to encode.")

# Function to decode a QR code image
def decode_qr_code():
    file_path = file_path_entry.get()
    if file_path:
        try:
            image = cv2.imread(file_path)
            detector = cv2.QRCodeDetector()
            val, pts, qr_code = detector.detectAndDecode(image)
            if val:
                decoded_text.config(state=tk.NORMAL)
                decoded_text.delete(1.0, tk.END)
                decoded_text.insert(tk.END, val)
                decoded_text.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", "No QR code found in the image.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please select an image to decode.")

# Function to open a file dialog to select an image for decoding
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

# Create the main window
root = tk.Tk()
root.title("QR Code Encoder and Decoder")

# Create and configure the notebook
notebook = ttk.Notebook(root)
encode_frame = ttk.Frame(notebook)
decode_frame = ttk.Frame(notebook)

# Add the frames to the notebook
notebook.add(encode_frame, text="Encode")
notebook.add(decode_frame, text="Decode")
notebook.pack(padx=10, pady=10, fill="both", expand=True)

# Encode Frame
text_label = ttk.Label(encode_frame, text="Enter text to encode:")
text_label.pack(pady=10)
text_entry = ttk.Entry(encode_frame, width=40)
text_entry.pack()
encode_button = ttk.Button(encode_frame, text="Encode", command=encode_text)
encode_button.pack(pady=10)

# Decode Frame
file_path_label = ttk.Label(decode_frame, text="Select an image to decode:")
file_path_label.pack(pady=10)
file_path_entry = ttk.Entry(decode_frame, width=30)
file_path_entry.pack()
browse_button = ttk.Button(decode_frame, text="Browse", command=select_image)
browse_button.pack(pady=10)
decode_button = ttk.Button(decode_frame, text="Decode", command=decode_qr_code)
decode_button.pack(pady=10)
decoded_text = tk.Text(decode_frame, height=5, width=40, state=tk.DISABLED)
decoded_text.pack(pady=10)

# QR Code Display
qr_code_label = ttk.Label(root)
qr_code_label.pack(pady=10)

# Start the GUI main loop
root.mainloop()
