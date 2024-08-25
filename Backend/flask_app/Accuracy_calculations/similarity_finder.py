import numpy as np
import pandas as pd

def load_reference_data(shot_type):

    stats_directory = f'D:/SLIIT/Academic/YEAR 04/Research/Training/newData/{shot_type}.csv'
    reference_data = pd.read_csv(stats_directory)
    
    # Define the distance columns
    distance_columns = [
        'left_shoulder_right_shoulder',
        'right_shoulder_right_elbow',
        'right_shoulder_right_hip',
        'left_hip_right_hip',
        'right_hip_right_knee',
        'right_knee_right_ankle'
    ]
    
    return reference_data[distance_columns + ['image_name']]  # Ensure 'image_name' is included

def find_closest_match(user_distances, shot_type):

    if shot_type == 'backfoot defence':
        shot_type = 'backfoot_defence'
    elif shot_type == 'backfoot drive':
        shot_type = 'backfoot_drive'
    elif shot_type == 'forward defence':
        shot_type = 'forward_defence'
    elif shot_type == 'forward drive':
        shot_type = 'forward_drive'

    # Load the reference data for the given shot type
    reference_data = load_reference_data(shot_type)

    print(shot_type)
    min_distance = float('inf')
    closest_image_name = None

    for index, row in reference_data.iterrows():
        reference_distances = {
            'left_shoulder_right_shoulder': row['left_shoulder_right_shoulder'],
            'right_shoulder_right_elbow': row['right_shoulder_right_elbow'],
            'right_shoulder_right_hip': row['right_shoulder_right_hip'],
            'left_hip_right_hip': row['left_hip_right_hip'],
            'right_hip_right_knee': row['right_hip_right_knee'],
            'right_knee_right_ankle': row['right_knee_right_ankle'],
        }
        
        # Calculate Euclidean distance between user and reference distances
        distance = np.linalg.norm(np.array(list(user_distances.values())) - np.array(list(reference_distances.values())))
        
        if distance < min_distance:
            min_distance = distance
            closest_image_name = row['image_name']

    print(min_distance, closest_image_name)

    return closest_image_name
