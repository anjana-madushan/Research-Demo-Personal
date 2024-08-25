import pandas as pd
import numpy as np

stats_directory = 'D:/SLIIT/Academic/YEAR 04/Research/Training/newData'

def calculate_accuracy_and_mae(shot_type, input_angles, matching_one):
    print(matching_one)
    
    stats_files_for_batting_shots = {
        'forward defence': 'forward_defence.csv',
        'forward drive': 'forward_drive.csv',
        'backfoot defence': 'backfoot_defence.csv',
        'backfoot drive': 'backfoot_drive.csv'
    }

    deviation_thresholds = {
        'angle_right_elbow': (10.0, 20.0),
        'angle_left_elbow': (10.0, 20.0),
        'angle_right_shoulder': (10.0, 20.0),
        'angle_left_knee': (10.0, 20.0),
        'angle_right_knee': (10.0, 20.0),
        'angle_right_hip_knee': (10.0, 20.0),
        'angle_left_hip_knee': (10.0, 20.0),
        'angle_right_hip_shoulder': (10.0, 20.0),
        'angle_right_shank': (10.0, 20.0),
        'angle_left_shank': (10.0, 20.0)
    }

    if shot_type not in stats_files_for_batting_shots:
        raise ValueError(f"Unknown batting shot: {shot_type}")

    stats_file = f'{stats_directory}/{stats_files_for_batting_shots[shot_type]}'
    stats_data = pd.read_csv(stats_file)

    print('stats_file', stats_file)
    print('stats_data columns:', stats_data.columns)
    print('stats_data head:', stats_data.head())

    matching_row = stats_data[stats_data['image_name'] == matching_one]
    if matching_row.empty:
        raise ValueError(f"No matching row found for image_name {matching_one}")

    print('matching_row columns:', matching_row.columns)
    print('matching_row:', matching_row)

    angle_columns = [col for col in stats_data.columns if 'distance' not in col]
    print("angle_columns", angle_columns)

    # Specify the columns you want to remove
    columns_to_remove = ['left_shoulder_right_shoulder', 'right_shoulder_right_elbow', 'right_shoulder_right_hip', 'left_hip_right_hip', 'right_hip_right_knee', 'right_knee_right_ankle', 'label']

    # Check which columns exist before attempting to drop them
    existing_columns_to_remove = [col for col in columns_to_remove if col in matching_row.columns]
    print("Existing columns to remove", existing_columns_to_remove)

    matching_row = matching_row.drop(columns=existing_columns_to_remove, errors='ignore')
    print('matching_row after dropping columns', matching_row)

    # Ensure matching_row is still valid and contains the necessary columns
    angle_columns_in_matching_row = [col for col in angle_columns if col in matching_row.columns]
    print("Angle columns in matching row:", angle_columns_in_matching_row)

    if not angle_columns_in_matching_row:
        raise ValueError("No valid angle columns available in the matching row")

    matching_angles = matching_row[angle_columns_in_matching_row].iloc[0].to_dict()  # Use iloc[0] to get the first row as a Series
    print('matching_angles', matching_angles)
    print('input_angles', input_angles)

    if not set(input_angles.keys()).issubset(set(angle_columns_in_matching_row)):
        raise ValueError("Input angles do not match the angle columns in the reference data")

    result = categorize_and_calculate_mae(input_angles, matching_angles, deviation_thresholds)

    return result

def categorize_and_calculate_mae(input_angles, reference_angles, deviation_thresholds):
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

            if error <= accurate_threshold:
                correctness.append(100)
            elif error <= minor_error_threshold:
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
    print(mae_percentage)

    # Generate rectification messages based on angles needing correction
    rectifications = generate_rectification_messages(
        rectification_needed.items(),
        reference_angles,  
        deviation_thresholds  
    )

    result = {
        'Accuracy': mae_percentage,
        # 'False Joints': false_joints,
        # 'Incorrect Angles': incorrect_angles,
        'Rectification Messages': rectifications
    }

    return result

def generate_rectification_messages(rectification_needed_items, reference_angles, deviation_thresholds):
    rectifications = []

    for angle_name, input_value in rectification_needed_items:
        if angle_name in reference_angles and angle_name in deviation_thresholds:
            reference_value = reference_angles[angle_name]
            accurate_threshold, minor_error_threshold = deviation_thresholds[angle_name]

            if abs(input_value - reference_value) <= minor_error_threshold:
                message = {
                    'angle name': angle_name,
                    'error type': 'minor error',
                    'current angle value': round(input_value),
                    'general response': (f"Your {angle_name} is slightly off. "
                                         f"Try to adjust it to reduce the minor deviation."),
                    'mathematical response': (f"Correct the angle to be closer to the reference value.")
                }
            else:
                if input_value > reference_value:
                    direction = "too wide"
                    correction = "Make it narrower"
                else:
                    direction = "too narrow"
                    correction = "Make it wider"
                
                message = {
                    'angle name': angle_name,
                    'error type': 'large error',
                    'current angle value': round(input_value),
                    'general response': (f"Your {angle_name} is {direction}. "
                                         f"{correction} to reduce the deviation."),
                    'mathematical response': (f"Adjust it to be within the acceptable range.")
                }

            rectifications.append(message)

    return rectifications