import numpy as np

def shankAngleCalculate(shank_vector, reference_vector):
    # Calculate dot product
    dot_product = np.dot(shank_vector, reference_vector)
    
    # Calculate magnitudes
    magnitude1 = np.linalg.norm(shank_vector)
    magnitude2 = np.linalg.norm(reference_vector)
    
    # Calculate angle in radians
    radians = np.arccos(dot_product / (magnitude1 * magnitude2))
    
    # Convert radians to degrees
    degrees = np.degrees(radians)

    final_angle_value = 180-degrees
    
    return final_angle_value