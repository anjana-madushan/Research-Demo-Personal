import pandas as pd
import numpy as np

stats_directory = 'D:/SLIIT/Academic/YEAR 04/Research/Training/newData'

def calculate_accuracy_and_mae(shot_type, input_angles, closet_matches):
    stats_files_for_batting_shots = {
        'forward defence': 'forward_defence.csv',
        'forward drive': 'forward_drive.csv',
        'backfoot defence': 'backfoot_defence.csv',
        'backfoot drive': 'backfoot_drive.csv'
    }

    if shot_type not in stats_files_for_batting_shots:
        raise ValueError(f"Unknown batting shot: {shot_type}")

    stats_file = f'{stats_directory}/{stats_files_for_batting_shots[shot_type]}'
    stats_data = pd.read_csv(stats_file)

    # Ensure closet_matches is a DataFrame
    closet_matches = pd.DataFrame(closet_matches)

    # Compute averages and standard deviations for each angle column
    angle_columns = [col for col in stats_data.columns if 'angle' in col]
    matching_angles_data = closet_matches[angle_columns]

    mean_values = matching_angles_data.mean()
    std_values = matching_angles_data.std()

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
    result = categorize_and_calculate_mae(input_angles, mean_values.to_dict(), deviation_thresholds)

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
        deviation_thresholds
    )

    result = {
        'Accuracy': mae_percentage,
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