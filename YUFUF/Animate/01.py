import cv2
import numpy as np

# Load your image
image = cv2.imread('your_image.jpg')
height, width = image.shape[:2]

# Animation parameters
frames = 60
zoom_factor = 1.05  # Slight zoom per frame
pan_step = 2        # Pixels to pan per frame

for i in range(frames):
    # Calculate zoom
    scale = zoom_factor ** i
    new_width = int(width / scale)
    new_height = int(height / scale)

    # Crop center
    x1 = int((width - new_width) / 2) + pan_step * i
    y1 = int((height - new_height) / 2)
    x2 = x1 + new_width
    y2 = y1 + new_height

    # Ensure bounds
    x1 = max(0, min(x1, width - new_width))
    y1 = max(0, min(y1, height - new_height))

    cropped = image[y1:y2, x1:x2]
    resized = cv2.resize(cropped, (width, height))

    # Show frame
    cv2.imshow('Animated Image', resized)
    cv2.waitKey(50)  # Delay in milliseconds

cv2.destroyAllWindows()
