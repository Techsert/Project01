import os
from PIL import Image

# Tolerance for near-white detection
tolerance = 50

# Get current working directory (where the script is running)
folder = os.getcwd()

for filename in os.listdir(folder):
    if filename.lower().endswith(".png"):
        img = Image.open(filename).convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            r, g, b, a = item
            if r > tolerance and g > tolerance and b > tolerance:
                newData.append((255, 255, 255, 0))  # Transparent
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(filename, "PNG")  # Overwrite original file
        print(f"Updated: {filename}")
