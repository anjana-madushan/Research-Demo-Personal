import pandas as pd
import numpy as np

stats_directory = 'D:/SLIIT/Academic/YEAR 04/Research/Training/newData'

def calculate_accuracy_and_mae(shot_type, input_angles, closet_matches, batsman_type):

    closet_matches = pd.DataFrame(closet_matches)

    mean_values = closet_matches.mean()
    std_values = closet_matches.std()

    angle_columns = closet_matches.columns.tolist()
    # Define deviation thresholds based on the standard deviations
    deviation_thresholds = {
        angle: (mean_values[angle], std_values[angle])
        for angle in angle_columns
        if angle in mean_values
    }

    # Check for empty deviation thresholds
    if not deviation_thresholds:
        raise ValueError("No valid deviation thresholds available")

    # Use the updated deviation thresholds in the calculation
    result = categorize_and_calculate_mae(input_angles, mean_values.to_dict(), deviation_thresholds, batsman_type)

    return result

def categorize_and_calculate_mae(input_angles, reference_angles, deviation_thresholds, batsman_type):
    absolute_deviations = []
    false_joints = {}
    incorrect_angles = {}
    rectification_needed = {}
    correctness = []

    total_error = 0
    count = 0

    for angle, input_value in input_angles.items():
        if angle in reference_angles:
            reference_value = reference_angles[angle]
            accurate_threshold, minor_error_threshold = deviation_thresholds.get(angle, (float('inf'), float('inf')))

            error = abs(input_value - reference_value)

            if error <= minor_error_threshold and abs(input_value)<abs(accurate_threshold):
                correctness.append(100)
            elif error >= minor_error_threshold and error < 2*minor_error_threshold:
                absolute_deviations.append(error)
                false_joints[angle] = input_value
                rectification_needed[angle] = input_value
                total_error += error
                count += 1
            else:
                incorrect_angles[angle] = input_value
                rectification_needed[angle] = input_value
                correctness.append(0)

    overall_mae = sum(absolute_deviations) / len(absolute_deviations) if absolute_deviations else 0
    mae_percentage = round(100 - overall_mae)  
    
    rectifications = generate_rectification_messages(
        rectification_needed.items(),
        reference_angles,
        deviation_thresholds, 
        batsman_type,
        input_angles
    )

    result = {
        'Accuracy': mae_percentage,
        'Rectification Messages': rectifications
    }

    return result


def generate_rectification_messages(rectification_needed_items, reference_angles, deviation_thresholds, batsman_type, input_angles):
    rectifications = []

    neighboring_joints = {
        'angle_right_elbow': ['RIGHT SHOULDER', 'RIGHT WRIST'],
        'angle_left_elbow': ['LEFT SHOULDER', 'LEFT WRIST'],
        'angle_right_shoulder': ['RIGHT HIP', 'RIGHT SHOULDER'],
        'angle_left_knee': ['LEFT HIP', 'LEFT ANKLE'],
        'angle_right_knee': ['RIGHT HIP', 'RIGHT ANKLE'],
        'angle_right_hip_knee': ['RIGHT KNEE', 'LEFT HIP'],
        'angle_right_hip_shoulder': ['RIGHT_KNEE', 'RIGHT SHOULDER'],
        'angle_right_shank': ['RIGHT ANKLE', 'LEFT ANKLE'],
        'angle_left_shank': ['LEFT ANKLE', 'RIGHT ANKLE']
    }

    for angle_name, input_value in rectification_needed_items:
        
        mapped_angle_name = map_angle_names(angle_name, batsman_type)
        
        if angle_name in reference_angles and angle_name in deviation_thresholds:
            reference_value = reference_angles[angle_name]
            accurate_threshold, minor_error_threshold = deviation_thresholds[angle_name]

            error = abs(input_value - reference_value)

            if error > minor_error_threshold:
                error_type = "large error"
                if input_value > reference_value:
                    error_description = "too wide"
                else:
                    error_description = "too narrow"
            else:
                error_type = "minor error"
                if abs(input_value - reference_value) < accurate_threshold:
                    error_description = "narrow"
                else:
                    error_description = "wide"

            lower_bound = round(reference_value - minor_error_threshold)
            upper_bound = round(reference_value + minor_error_threshold)
            acceptable_range = f"{lower_bound}° to {upper_bound}°"
            
            # Provide feedback based on neighboring joints
            neighbors = neighboring_joints.get(angle_name, [])
            print(neighbors)
            # feedback = check_neighboring_joints(angle_name, input_angles, neighbors)

            message = {
                'angle name': mapped_angle_name,
                'current angle value': round(input_value),
                'acceptable range': acceptable_range,
                'error type': error_type,
                'error description': error_description,
                'neighboring joints to change': neighbors
            }

            rectifications.append(message)

            # if abs(input_value - reference_value) <= minor_error_threshold:
            #     message = {
            #         'angle name': mapped_angle_name,
            #         'error type': 'minor error',
            #         'current angle value': round(input_value),
            #         'general response': (f"Your {angle_name} is slightly off. "
            #                              f"Try to adjust it to reduce the minor deviation."),
            #         'mathematical response': (f"Correct the angle to be closer to the reference value.")
            #     }
            # else:
            #     if input_value > reference_value:
            #         direction = "too wide"
            #         correction = "Make it narrower"
            #     else:
            #         direction = "too narrow"
            #         correction = "Make it wider"
                
            #     message = {
            #         'angle name': mapped_angle_name,
            #         'error type': 'large error',
            #         'current angle value': round(input_value),
            #         'general response': (f"Your {angle_name} is {direction}. "
            #                              f"{correction} to reduce the deviation."),
            #         'mathematical response': (f"Adjust it to be within the acceptable range.")
            #     }

    return rectifications

def map_angle_names(angle_name, batsman_type):
    if batsman_type == 'left-hand':
        # Swap right with left for left-hand batsmen
        angle_name = angle_name.replace('right_', 'temp_').replace('left_', 'right_').replace('temp_', 'left_')

    return angle_name

def check_neighboring_joints(angle_name, input_angles, neighbors):
    # Limit feedback to the first 2 neighboring joints
    feedback = []
    for neighbor in neighbors[:2]:  # Take only the first 2 neighbors
        if neighbor in input_angles:
            print('neigbour', neighbor)
            feedback.append(neighbor)
    
    return feedback