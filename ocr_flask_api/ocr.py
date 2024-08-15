from PIL import Image, ImageDraw, ImageOps
import cv2
import numpy as np

# Path to your image file
image_path = 'screenshot.png'

try:
    # Open original image using PIL
    image_pil = Image.open(image_path)

    # Convert the image to RGBA mode
    image_pil = image_pil.convert("RGBA")

    # Convert PIL image to OpenCV format for edge detection
    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGBA2BGR)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection or other methods to detect the strikethrough line
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Hough Line Transform to detect lines in the image
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

    # Create a blank mask image for transparency
    mask = np.ones_like(image_cv) * 255  # Initialize mask with white pixels

    # Draw detected lines on the mask (black lines to remove)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(mask, (x1, y1), (x2, y2), (0, 0, 0), 2)  # Black line on the mask

    # Invert the mask (white lines to keep)
    mask = cv2.bitwise_not(mask)

    # Convert mask to PIL Image format
    mask_pil = Image.fromarray(mask)

    # Apply the mask as alpha channel to the image
    image_pil.putalpha(mask_pil)

    # Save or display the result
    image_pil.show()

except Exception as e:
    print(f"Error loading or processing image: {e}")
