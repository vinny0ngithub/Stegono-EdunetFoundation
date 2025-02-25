import cv2
import string
import os
from PIL import Image  # Additional module for image conversion

# Take inputs
cover_file = input("Enter cover image filename: ")

# Load the image with PIL to handle various formats and convert to PNG
try:
    with Image.open(cover_file) as img_pil:
        # Convert to RGB (ensures compatibility with cv2)
        img_pil = img_pil.convert('RGB')
        # If not PNG, save as a temporary PNG file
        if not cover_file.lower().endswith('.png'):
            temp_png = cover_file.rsplit('.', 1)[0] + '_temp.png'
            img_pil.save(temp_png, 'PNG')
            print(f"Converted {cover_file} to {temp_png} for compatibility.")
            cover_file = temp_png
except Exception as e:
    print(f"Error loading or converting image: {e}")
    exit()

# Load the image with cv2 (now guaranteed to be PNG-compatible)
img = cv2.imread(cover_file)
if img is None:
    print("Error: Could not load image with cv2")
    exit()

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Create dictionaries for character-to-ASCII and vice versa
d = {chr(i): i for i in range(255)}
c = {i: chr(i) for i in range(255)}

# Prepare data to embed: length (4 digits) + password + message
length = len(msg)
length_str = str(length).zfill(4)
to_embed = length_str + password + msg

# Embed data into the image
m = 0  # Row
n = 0  # Column
z = 0  # Channel (B=0, G=1, R=2)

for i in range(len(to_embed)):
    if n >= img.shape[0] or m >= img.shape[1]:
        print("Error: Image too small to hold the data")
        exit()
    img[n, m, z] = d[to_embed[i]]
    n += 1
    m += 1
    z = (z + 1) % 3

# Save the stego image
stego_file = input("Enter output stego image filename (will be saved as PNG): ")
if not stego_file.lower().endswith('.png'):
    stego_file += '.png'  # Force PNG extension
cv2.imwrite(stego_file, img)
print(f"Message embedded and saved to {stego_file}")

# Open the image (Linux-compatible; adjust or comment out if not needed)
os.system(f"xdg-open {stego_file}")

# Clean up temporary file if created
if 'temp_png' in locals():
    try:
        os.remove(temp_png)
        print(f"Cleaned up temporary file: {temp_png}")
    except:
        print("Warning: Could not remove temporary file")