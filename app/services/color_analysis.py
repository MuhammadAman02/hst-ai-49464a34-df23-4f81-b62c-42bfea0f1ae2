import cv2
import numpy as np
from skimage import color
from PIL import Image
import io

def extract_skin_tone(image):
    # Convert image to LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Define range for skin color in LAB space
    lower = np.array([20, 130, 120], dtype=np.uint8)
    upper = np.array([220, 180, 180], dtype=np.uint8)
    
    # Create a mask for skin color
    skin_mask = cv2.inRange(lab_image, lower, upper)
    
    # Apply the mask to the original image
    skin = cv2.bitwise_and(image, image, mask=skin_mask)
    
    # Calculate the average color of the skin
    return np.mean(skin, axis=(0, 1))

def get_complementary_color(color):
    # Convert RGB to HSV
    hsv = color.rgb2hsv(color.reshape(1, 1, 3))
    
    # Calculate complementary color
    hsv[0, 0, 0] = (hsv[0, 0, 0] + 0.5) % 1.0
    
    # Convert back to RGB
    return color.hsv2rgb(hsv)[0, 0]

def get_color_palette(skin_tone):
    # Normalize skin tone
    skin_tone = skin_tone / 255.0
    
    # Get complementary color
    complementary = get_complementary_color(skin_tone)
    
    # Generate a simple color palette
    palette = [
        skin_tone,
        complementary,
        np.clip(skin_tone * 1.5, 0, 1),  # Lighter shade
        np.clip(skin_tone * 0.5, 0, 1),  # Darker shade
        np.clip(complementary * 1.5, 0, 1),  # Lighter complementary
    ]
    
    return [(int(r*255), int(g*255), int(b*255)) for r, g, b in palette]

def change_skin_tone(image, target_tone):
    # Convert image to LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image into L, A, and B channels
    l, a, b = cv2.split(lab_image)
    
    # Adjust the L channel (lightness)
    l = np.clip(l * (target_tone[0] / 128.0), 0, 255).astype(np.uint8)
    
    # Merge the channels back
    adjusted_lab = cv2.merge((l, a, b))
    
    # Convert back to BGR color space
    return cv2.cvtColor(adjusted_lab, cv2.COLOR_LAB2BGR)

def process_image(file):
    # Read image file
    image_data = file.file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Extract skin tone
    skin_tone = extract_skin_tone(image)
    
    # Get color palette
    palette = get_color_palette(skin_tone)
    
    return image, skin_tone, palette

def change_image_skin_tone(file, target_tone):
    # Read image file
    image_data = file.file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Change skin tone
    adjusted_image = change_skin_tone(image, target_tone)
    
    # Convert image to bytes
    is_success, buffer = cv2.imencode(".png", adjusted_image)
    io_buf = io.BytesIO(buffer)
    
    return io_buf