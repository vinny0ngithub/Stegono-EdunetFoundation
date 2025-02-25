import cv2
import string
import os
from PIL import Image  # Additional module for image conversion

# Take inputs
stego_file = input("Enter stego image filename: ")

# Load the image with PIL to handle various formats and convert to PNG
try:
    with Image.open(stego_file) as img_pil:
        # Convert to RGB (ensures compatibility with cv2)
        img_pil = img_pil.convert('RGB')
        # If not PNG, save as a temporary PNG file
        if not stego_file.lower().endswith('.png'):
            temp_png = stego_file.rsplit('.', 1)[0] + '_temp.png'
            img_pil.save(temp_png, 'PNG')
            print(f"Converted {stego_file} to {temp_png} for compatibility.")
            stego_file = temp_png
except Exception as e:
    print(f"Error loading or converting image: {e}")
    exit()

# Load the image with cv2 (now guaranteed to be PNG-compatible)
img = cv2.imread(stego_file)
if img is None:
    print("Error: Could not load image with cv2")
    exit()

pas = input("Enter passcode for Decryption: ")

# Create dictionary for ASCII-to-character mapping
c = {i: chr(i) for i in range(255)}

# Initialize coordinates
m = 0
n = 0
z = 0

# Extract length (first 4 characters)
length_str = ""
pixel_values = []  # For debugging
for i in range(4):
    if n >= img.shape[0] or m >= img.shape[1]:
        print("Error: Image too small")
        exit()
    pixel_value = img[n, m, z]
    pixel_values.append(pixel_value)
    length_str += c[pixel_value]
    n += 1
    m += 1
    z = (z + 1) % 3

# Debug output
print("Extracted pixel values:", pixel_values)
print("Extracted length_str:", repr(length_str))
try:
    length = int(length_str)
except ValueError:
    print("Error: Invalid length data")
    exit()

# Extract password
password_extracted = ""
password_length = len(pas)
for i in range(password_length):
    if n >= img.shape[0] or m >= img.shape[1]:
        print("Error: Image too small")
        exit()
    password_extracted += c[img[n, m, z]]
    n += 1
    m += 1
    z = (z + 1) % 3

# Verify password and extract message
if pas == password_extracted:
    message = ""
    for i in range(length):
        if n >= img.shape[0] or m >= img.shape[1]:
            print("Error: Image too small")
            exit()
        message += c[img[n, m, z]]
        n += 1
        m += 1
        z = (z + 1) % 3
    print("Decryption message:", message)
else:
    print("YOU ARE NOT auth")

# Clean up temporary file if created
if 'temp_png' in locals():
    try:
        os.remove(temp_png)
        print(f"Cleaned up temporary file: {temp_png}")
    except:
        print("Warning: Could not remove temporary file")