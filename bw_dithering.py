import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

#function for selecting the image file path via a dialogue box
def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if filename:
        image_path.set(filename)
        load_image()

#function, which fetches the image path and opens it
def load_image():
    image_path_value = image_path.get()
    if image_path_value:
        global image
        image = Image.open(image_path_value)
        display_image(image, original_label)


#it displays the loaded image
def display_image(img, label):
    img_width, img_height = img.size
    max_size = 200
    if img_width > max_size or img_height > max_size:     # Scales the image, so that it can fit on the screen
        scale = min(max_size / img_width, max_size / img_height)
        img = img.resize((int(img_width * scale), int(img_height * scale)), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo

#checks if an image has been selected and moves on with the conversion
def start_conversion():
    if not image:
        messagebox.showerror("Error", "No image loaded.")
        return
    convert_image()

#gets the selected algorithm and calls the respective fucntion for image conversion
def convert_image():
    grayscale_image = image.convert("L")
    algorithm_value = algorithm.get()

    if algorithm_value == "Threshold":
            threshold = threshold_value.get()
            if not (0 <= threshold <= 255):
                raise ValueError("Threshold must be between 0 and 255.")
            global dithered_image
            dithered_image = threshold_dithering(grayscale_image, threshold)

    elif algorithm_value == "Random":
        dithered_image = random_dithering(grayscale_image)
    
    else:
        messagebox.showerror("Error", "Select a model")

    
    display_image(dithered_image, dithered_label)


def threshold_dithering(img, threshold):
    img_array = np.array(img)
    dithered_array = (img_array > threshold) * 255
    return Image.fromarray(dithered_array.astype(np.uint8))

def random_dithering(img):
    img_array = np.array(img)
    random_matrix = np.random.rand(*img_array.shape) * 255
    dithered_array = (img_array > random_matrix) * 255
    return Image.fromarray(dithered_array.astype(np.uint8))

#promts the user the save the image to a specified path
def save_dithered_image():
    if dithered_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".tif", filetypes=[("TIFF files", "*.tif")])
        if save_path:
            dithered_image.save(save_path)
    else:
        messagebox.showerror("Error", "No dithered image to save.")


#gui window creation
root = tk.Tk()

#title
root.title("B&W Dithering Editor")

#getting value from user
image_path = tk.StringVar()
algorithm = tk.StringVar(value="Threshold")
threshold_value = tk.DoubleVar(value=128.0)


# Image path entry and file selection button
tk.Label(root, text="Image Path:").grid(row=0, column=0, sticky='e')
tk.Entry(root, textvariable=image_path, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2)

# Algorithm selection
tk.Label(root, text="Algorithm:").grid(row=1, column=0, sticky='e')
ttk.OptionMenu(root, algorithm, "Select", "Threshold", "Random").grid(row=1, column=1)

# Threshold parameter entry
tk.Label(root, text="Threshold:").grid(row=2, column=0, sticky='e')
threshold_entry = tk.Entry(root, textvariable=threshold_value)
threshold_entry.grid(row=2, column=1)

# Generate and Save buttons
tk.Button(root, text="Generate", command=start_conversion).grid(row=3, column=0, columnspan=3)
tk.Button(root, text="Save Dithered Image", command=save_dithered_image).grid(row=4, column=0, columnspan=3)

# Image display
original_label = tk.Label(root)
original_label.grid(row=5, column=0, columnspan=3)

dithered_label = tk.Label(root)
dithered_label.grid(row=6, column=0, columnspan=3)

root.mainloop()
