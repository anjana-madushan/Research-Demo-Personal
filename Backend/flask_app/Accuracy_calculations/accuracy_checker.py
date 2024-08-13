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
                    'angle name': angle_name,
                    'error type': error_type,
                    'general reponse': (f"Your {angle_name_formatted} is too narrow. "
                                               f"Make it wider"),
                    'current angle value':round(input_angle_value),
                    'mathematical response':(f"Adjust it to be between {round(first_sd_lower)} degree and {round(first_sd_upper)} degrees.")
                }
            else:
                message = {
                    'angle name': angle_name,
                    'error type': error_type,
                    'general reponse': (f"Your {angle_name_formatted} is too wide. "
                                               f"Make it narrow"),
                    'current angle_value':(f"{round(input_angle_value)}°"),
                    'mathematical_response':(f"Adjust it to be between {round(first_sd_lower)} degree and {round(first_sd_upper)} degrees.")
                }
            rectifications.append(message)
    
    return rectifications

def calculate_mae_accuracy(average_angle_status, tolerances, input_angles, stats_data):
    absolute_deviations = []
    false_joints = {}
    incorrect_angles = {}
    rectification_needed = {}
    correctness = []

    for angle_name, input_angle_value in input_angles:
        if angle_name in average_angle_status['Angle'].values:
            avg_value = stats_data.loc[stats_data['Angle'] == angle_name, 'Average'].values[0]
            lower_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'Lower_tolerance'].values[0]
            upper_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'Upper_tolerance'].values[0]
            first_sd_lower = tolerances.loc[tolerances['Angle'] == angle_name, 'First_SD_Lower'].values[0]
            first_sd_upper = tolerances.loc[tolerances['Angle'] == angle_name, 'First_SD_Upper'].values[0]

            absolute_deviation = abs(input_angle_value - avg_value)

            if lower_tolerance <= input_angle_value <= upper_tolerance:
                if first_sd_lower <= input_angle_value <= first_sd_upper:
                    correctness.append(100)
                else:
                    # Append the absolute deviation to calculate MAE
                    absolute_deviations.append(absolute_deviation)
                    false_joints[angle_name] = input_angle_value
                    rectification_needed[angle_name] = input_angle_value
            else:
                # Handle angles outside the tolerance range
                correctness.append(0)
                incorrect_angles[angle_name] = input_angle_value
                rectification_needed[angle_name] = input_angle_value

    overall_mae = sum(absolute_deviations) / len(absolute_deviations) if absolute_deviations else 0
    print(overall_mae)
    # Calculate the accuracy based on MAE
    considered_joints_accuracy = round(100 - overall_mae)  # Convert MAE to a percentage accuracy

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
