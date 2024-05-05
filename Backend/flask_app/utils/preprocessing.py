import cv2
import numpy as np

def preprocess_image(image):
    # Apply Gaussian Blur to remove blur
    blurred_image = cv2.GaussianBlur(image, (7, 7), 0)
    
    # Apply Median Blur to remove salt-and-pepper noise
    median_blurred_image = cv2.medianBlur(blurred_image, 5)
    
    # Perform resizing and cropping if necessary
    resized_image = cv2.resize(median_blurred_image, (224, 224))
    
    # Normalize pixel values to range [0, 1]
    normalized_image = resized_image / 255.0
    
    # Convert image to 8-bit unsigned integer depth
    uint8_image = (normalized_image * 255).astype(np.uint8)
    
    return uint8_image