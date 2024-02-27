import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Function to hide text within an image
def hide_text(image_path, text, output_path):
    try:
        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        binary_text = ''.join(format(ord(char), '08b') for char in text)
        if len(binary_text) > img.width * img.height:
            raise ValueError("Text is too long to hide in the image.")
        pixels = list(img.getdata())
        index = 0
        for i in range(len(pixels)):
            r, g, b, a = pixels[i]
            if index < len(binary_text):
                bit = int(binary_text[index])
                a = (a & 254) | bit
                pixels[i] = (r, g, b, a)
                index += 1
        img.putdata(pixels)
        img.save(output_path)
        print("Text hidden successfully.")
        return True
    except Exception as e:
        print("Error:", e)
        return False

# Function to extract text from a steganographic image
def extract_text(image_path):
    try:
        img = Image.open(image_path)
        if img.mode != 'RGBA':
            raise ValueError("Image must be in RGBA mode to extract text.")
        pixels = list(img.getdata())
        binary_text = ''
        for pixel in pixels:
            binary_text += str(pixel[3] & 1)
        text = ''
        for i in range(0, len(binary_text), 8):
            byte = binary_text[i:i+8]
            text += chr(int(byte, 2))
        return text
    except Exception as e:
        print("Error:", e)
        return None

# Event handler for hiding text within an image
def encrypt_text():
    image_path = file_entry.get()
    text = text_entry.get("1.0", tk.END).strip()
    if image_path and text:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            success = hide_text(image_path, text, output_path)
            output_label.config(text="Text hidden successfully." if success else "Error hiding text.", fg="green" if success else "red")
        else:
            output_label.config(text="Operation canceled.", fg="red")
    else:
        output_label.config(text="Please fill all fields.", fg="red")

# Event handler for extracting text from a steganographic image
def decrypt_text():
    image_path = file_entry_decrypt.get()
    if image_path:
        try:
            text = extract_text(image_path)
            if text:
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, text)
                output_label_decrypt.config(text="Text extracted successfully.", fg="green")
            else:
                output_label_decrypt.config(text="Error extracting text.", fg="red")
        except Exception as e:
            output_label_decrypt.config(text="Error: " + str(e), fg="red")
    else:
        output_label_decrypt.config(text="Please fill all fields.", fg="red")

# GUI setup
root = tk.Tk()
root.title("Steganography Tool")

# Encryption section
encrypt_frame = tk.Frame(root)
encrypt_frame.grid(row=0, column=0, padx=10, pady=10)

file_label = tk.Label(encrypt_frame, text="Choose Image:")
file_label.grid(row=0, column=0, padx=5, pady=5)
file_entry = tk.Entry(encrypt_frame, width=50)
file_entry.grid(row=0, column=1, padx=5, pady=5)
browse_button = tk.Button(encrypt_frame, text="Browse", command=lambda: file_entry.insert(tk.END, filedialog.askopenfilename()))
browse_button.grid(row=0, column=2, padx=5, pady=5)

text_label = tk.Label(encrypt_frame, text="Enter Text to Hide:")
text_label.grid(row=1, column=0, padx=5, pady=5)
text_entry = tk.Text(encrypt_frame, height=4, width=38)  # Adjusted width for consistency
text_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

encrypt_button = tk.Button(encrypt_frame, text="Encrypt", command=encrypt_text)
encrypt_button.grid(row=2, column=1, padx=5, pady=5)

output_label = tk.Label(encrypt_frame, text="", fg="green")
output_label.grid(row=3, column=1, padx=5, pady=5)

# Decryption section
decrypt_frame = tk.Frame(root)
decrypt_frame.grid(row=1, column=0, padx=10, pady=10)

file_label_decrypt = tk.Label(decrypt_frame, text="Choose Image:")
file_label_decrypt.grid(row=0, column=0, padx=5, pady=5)
file_entry_decrypt = tk.Entry(decrypt_frame, width=50)
file_entry_decrypt.grid(row=0, column=1, padx=5, pady=5)
browse_button_decrypt = tk.Button(decrypt_frame, text="Browse", command=lambda: file_entry_decrypt.insert(tk.END, filedialog.askopenfilename()))
browse_button_decrypt.grid(row=0, column=2, padx=5, pady=5)

decrypt_button = tk.Button(decrypt_frame, text="Decrypt", command=decrypt_text)
decrypt_button.grid(row=1, column=1, padx=5, pady=5)

output_text = tk.Text(decrypt_frame, height=4, width=38)  # Adjusted width for consistency
output_text.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

output_label_decrypt = tk.Label(decrypt_frame, text="", fg="green")
output_label_decrypt.grid(row=3, column=1, padx=5, pady=5)

root.mainloop()
