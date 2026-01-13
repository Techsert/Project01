from PIL import Image
import os

# Base folder (current folder where the script is)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "image_sizes.txt")

results = []

for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, BASE_DIR)
            try:
                with Image.open(path) as img:
                    w, h = img.size
                    ratio = round(w / h, 3) if h != 0 else "inf"
                    results.append(f"{rel_path} → {ratio}")
            except Exception as e:
                results.append(f"{rel_path} → ERROR: {e}")

# Save to text file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("📏 Image Aspect Ratio Report\n")
    f.write("=" * 40 + "\n\n")
    f.write("\n".join(results))

print(f"✅ Done! Ratios saved to: {OUTPUT_FILE}")
