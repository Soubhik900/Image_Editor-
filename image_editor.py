import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    beta = brightness  # Brightness adjustment
    alpha = contrast / 100.0 + 1  # Contrast scaling factor
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

def remove_noise(image):
    denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    return denoised

def process_image(image, brightness=0, contrast=0, denoise=False):
    if image is None:
        return None
    image = adjust_brightness_contrast(image, brightness, contrast)
    if denoise:
        image = remove_noise(image)
    return image

def open_image():
    global img, img_cv
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if not file_path:
        return
    img_cv = cv2.imread(file_path)
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    img_pil.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img_pil)
    canvas.create_image(200, 200, image=img)
    canvas.image = img

def apply_changes():
    global img, img_cv
    if img_cv is None:
        messagebox.showerror("Error", "No image loaded")
        return
    
    brightness = simpledialog.askinteger("Brightness", "Enter brightness (-100 to 100):", minvalue=-100, maxvalue=100, initialvalue=0)
    contrast = simpledialog.askinteger("Contrast", "Enter contrast (0 to 100):", minvalue=0, maxvalue=100, initialvalue=50)
    denoise = messagebox.askyesno("Noise Removal", "Do you want to apply noise removal?")
    
    processed = process_image(img_cv, brightness, contrast, denoise)
    img_pil = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
    img_pil.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img_pil)
    canvas.create_image(200, 200, image=img)
    canvas.image = img

def save_image():
    global img_cv
    if img_cv is None:
        messagebox.showerror("Error", "No image to save")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
    if not file_path:
        return
    cv2.imwrite(file_path, img_cv)
    messagebox.showinfo("Success", f"Image saved as {file_path}")

# Create GUI
root = tk.Tk()
root.title("Simple Image Editor")
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()
btn_open = tk.Button(root, text="Open Image", command=open_image)
btn_open.pack()
btn_apply = tk.Button(root, text="Apply Changes", command=apply_changes)
btn_apply.pack()
btn_save = tk.Button(root, text="Save Image", command=save_image)
btn_save.pack()

img = None
img_cv = None

root.mainloop()
