import pandas as pd
import json

stats_directory = 'D:/SLIIT/Academic/YEAR 04/Research/Training/Stats'

def calculate_tolerance_ranges(stats_data):
    # Define the tolerance ranges using mean ± SD and 2*SD
    tolerances = pd.DataFrame(index=stats_data.index)
    tolerances['Angle'] = stats_data['Angle']
    tolerances['Upper_tolerance'] = stats_data['Average'] + 2 * stats_data['Standard Deviation (All)']
    tolerances['Lower_tolerance'] = stats_data['Average'] - 2 * stats_data['Standard Deviation (All)']
    tolerances['First_SD_Upper'] = stats_data['Average'] + stats_data['Standard Deviation (All)']
    tolerances['First_SD_Lower'] = stats_data['Average'] - stats_data['Standard Deviation (All)']
    return tolerances

def check_angle_upper_lower_status(input_angles, averageStats):
    status = []
    angle_names = averageStats['Angle'].tolist()
    
    for angle_name, input_angle_value in input_angles:
        if angle_name in angle_names:
            avg_angle_value = averageStats.loc[averageStats['Angle'] == angle_name, 'Average'].values
            if len(avg_angle_value) > 0:
                avg_angle_value = avg_angle_value[0]
                
                if input_angle_value > avg_angle_value:
                    status_value = 1
                elif input_angle_value == avg_angle_value:
                    status_value = 0
                else:
                    status_value = -1

                status.append({
                    'Angle': angle_name,
                    'Status': status_value
                })
            else:
                print(f"Angle '{angle_name}' not found in averageStats.")
        else:
            print(f"Angle '{angle_name}' not in angle names.")
    
    result_df = pd.DataFrame(status)
    return result_df

def generate_rectification_messages(input_angles, stats_data, tolerances):
    rectifications = []
    
    for angle_name, input_angle_value in input_angles:
        if angle_name in tolerances['Angle'].values:
            # avg_value = stats_data.loc[stats_data['Angle'] == angle_name, 'Average'].values[0]
            first_sd_lower = tolerances.loc[tolerances['Angle'] == angle_name, 'First_SD_Lower'].values[0]
            first_sd_upper = tolerances.loc[tolerances['Angle'] == angle_name, 'First_SD_Upper'].values[0]
            lower_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'Lower_tolerance'].values[0]
            upper_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'Upper_tolerance'].values[0]

            if input_angle_value < lower_tolerance or input_angle_value > upper_tolerance:
                error_type = "large error"
            elif input_angle_value < first_sd_lower or input_angle_value > first_sd_upper:
                error_type = "major error"
            else:
                continue  

            angle_name_formatted = angle_name.replace('angle_', '').replace('_', ' ')

            if input_angle_value < first_sd_lower:
                message = {
                    'angle_name': angle_name,
                    'error_type': error_type,
                    'general_reponse': (f"Your {angle_name_formatted} is too narrow. "
                                               f"Make it wider"),
                    'current_angle_value':round(input_angle_value),
                    'mathematical_response':(f"Adjust it to be between {round(first_sd_lower)} and {round(first_sd_upper)}.")
                }
            else:
                message = {
                    'angle_name': angle_name,
                    'error_type': error_type,
                    'general_reponse': (f"Your {angle_name_formatted} is too wide. "
                                               f"Make it narrow"),
                    'current_angle_value':round(input_angle_value),
                    'mathematical_response':(f"Adjust it to be between {round(first_sd_lower)} and {round(first_sd_lower)}.")
                }
            rectifications.append(message)
    
    return rectifications

def calculate_mae_accuracy(average_angle_status, tolerances, input_angles, stats_data):
    correctness = []
    false_joints = {}
    incorrect_angles = {}
    rectification_needed = {}
    
    for angle_name, input_angle_value in input_angles:
        if angle_name in average_angle_status['Angle'].values:
            avg_value = stats_data.loc[stats_data['Angle'] == angle_name, 'Average'].values[0]
            lower_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'Lower_tolerance'].values[0]
            upper_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'Upper_tolerance'].values[0]
            first_sd_lower = tolerances.loc[tolerances['Angle'] == angle_name, 'First_SD_Lower'].values[0]
            first_sd_upper = tolerances.loc[tolerances['Angle'] == angle_name, 'First_SD_Upper'].values[0]

            if lower_tolerance <= input_angle_value <= upper_tolerance:
                if first_sd_lower <= input_angle_value <= first_sd_upper:
                    correct_percentage = 100
                else:
                    actual_deviation = abs(input_angle_value - avg_value)
                    max_possible_deviation = max(abs(avg_value - first_sd_lower), abs(avg_value - first_sd_upper))
                    error = (actual_deviation / max_possible_deviation) * 100 if max_possible_deviation != 0 else 100
                    correct_percentage = max(0, 100 - error)
                    false_joints[angle_name] = input_angle_value
                    rectification_needed[angle_name] = input_angle_value
            else:
                correct_percentage = 0
                incorrect_angles[angle_name] = input_angle_value
                rectification_needed[angle_name] = input_angle_value

            correctness.append(correct_percentage)
    
    overall_correctness = sum(correctness) / len(correctness) if correctness else 0
    considered_joints_accuracy = round(overall_correctness)

    # Generate rectification messages only for angles that need rectification
    rectifications = generate_rectification_messages(rectification_needed.items(), stats_data, tolerances)

    result = {
        'Accuracy': considered_joints_accuracy,
        'False Joints': false_joints,
        'Incorrect Angles': incorrect_angles,
        'Rectification Messages': rectifications
    }

    return result

def calculate_accuracy(shot_type, input_angles):
    stats_files_for_batting_shots = {
        'forward_defence': 'forward_defence_3dstats.csv',
        'forward_drive': 'forward_drive_3dstats.csv',
        'backfoot_defence': 'backfoot_defence_3dstats.csv',
        'backfoot_drive': 'backfoot_drive_3dstats.csv'
    }

    if shot_type not in stats_files_for_batting_shots:
        raise ValueError(f"Unknown batting shot: {shot_type}")
    
    stats_file = f'{stats_directory}/{stats_files_for_batting_shots[shot_type]}'
    stats_data = pd.read_csv(stats_file)

    # Calculate tolerance ranges using mean ± SD and 2*SD
    tolerances = calculate_tolerance_ranges(stats_data)
    input_angles_tuple = list(input_angles.items())
    average_angle_status = check_angle_upper_lower_status(input_angles_tuple, stats_data)

    # Calculate the accuracy using MAE within the defined tolerances
    result = calculate_mae_accuracy(average_angle_status, tolerances, input_angles_tuple, stats_data)

    return result['Accuracy'], result['Rectification Messages']
