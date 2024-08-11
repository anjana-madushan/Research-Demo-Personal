import pandas as pd

stats_directory = 'D:/SLIIT/Academic/YEAR 04/Research/ModelTraining/3dNewStats'

def calculate_tolerance_ranges(stats_data):
    
    tolerances = pd.DataFrame(index=stats_data.index)
    tolerances['Angle'] = stats_data['Angle']
    tolerances['Upper_tolerance_1'] = abs(stats_data['Average'] + (stats_data['Standard Deviation (All)']))
    tolerances['lower_tolerance_1'] = abs(stats_data['Average'] - (stats_data['Standard Deviation (All)']))
    tolerances['Upper_tolerance_2'] = abs(stats_data['Average'] + 2*(stats_data['Standard Deviation (All)']))
    tolerances['lower_tolerance_2'] = abs(stats_data['Average'] - 2*(stats_data['Standard Deviation (All)']))
    tolerances['Upper_tolerance_2.5'] = abs(stats_data['Average'] + 2.5*(stats_data['Standard Deviation (All)']))
    tolerances['lower_tolerance_2.5'] = abs(stats_data['Average'] - 2.5*(stats_data['Standard Deviation (All)']))
    # print(tolerances)
    return tolerances

def check_angle_upper_lower_status(input_angles, averageStats):
    status = []
    for angle_name, input_angle_value in input_angles:
        if angle_name in averageStats['Angle'].values:
            avg_angle_value = averageStats.loc[averageStats['Angle'] == angle_name, 'Average'].values[0]
            
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

    return pd.DataFrame(status)


def calculate_percentage_accuracy(average_angle_status, tolerances, input_angles, shot_stats):
    correctness = []
    considered_left_angles = 0
    considered_right_angles = 0
    considered_high_std_angles_dict = {}
    considered_low_std_angles_dict = {}
    totally_wrong_high_std_angles_dict = {}
    totally_wrong_low_std_angles_dict = {}
    false_joints = {}

    for angle_name, input_angle_value in input_angles:
        if angle_name in average_angle_status['Angle'].values:
            status = average_angle_status.loc[average_angle_status['Angle'] == angle_name, 'Status'].values[0]
            avg_value = shot_stats.loc[shot_stats['Angle'] == angle_name, 'Average'].values[0]
            upper_tolerance_1 = tolerances.loc[tolerances['Angle'] == angle_name, 'Upper_tolerance_1'].values[0]
            lower_tolerance_1 = tolerances.loc[tolerances['Angle'] == angle_name, 'lower_tolerance_1'].values[0]
            upper_tolerance_2 = tolerances.loc[tolerances['Angle'] == angle_name, 'Upper_tolerance_2'].values[0]
            lower_tolerance_2 = tolerances.loc[tolerances['Angle'] == angle_name, 'lower_tolerance_2'].values[0]
            upper_tolerance_end = tolerances.loc[tolerances['Angle'] == angle_name, 'Upper_tolerance_2.5'].values[0]
            lower_tolerance_end = tolerances.loc[tolerances['Angle'] == angle_name, 'lower_tolerance_2.5'].values[0]

            if status > 0:
                if lower_tolerance_1 <= input_angle_value <= upper_tolerance_1:
                    correct_percentage = 100
                elif upper_tolerance_1 < input_angle_value <= upper_tolerance_2:
                    actual_deviation = input_angle_value - avg_value
                    expected_deviation = upper_tolerance_2 - avg_value
                    error = (actual_deviation / expected_deviation) * 100 if expected_deviation != 0 else 100
                    correct_percentage = max(0, 100 - error)
                elif upper_tolerance_2 < input_angle_value <= upper_tolerance_end:
                    actual_deviation = input_angle_value - avg_value
                    expected_deviation = upper_tolerance_end - avg_value
                    error = (actual_deviation / expected_deviation) * 100 if expected_deviation != 0 else 100
                    correct_percentage = max(0, 100 - error)
                else:
                    print('Do Not Consider: ', angle_name)
                    continue
            else:
                if lower_tolerance_end <= input_angle_value <= lower_tolerance_1:
                    correct_percentage = 100
                elif lower_tolerance_2 <= input_angle_value < lower_tolerance_1:
                    actual_deviation = avg_value - input_angle_value
                    expected_deviation = avg_value - lower_tolerance_2
                    error = (actual_deviation / expected_deviation) * 100 if expected_deviation != 0 else 100
                    correct_percentage = max(0, 100 - error)
                elif lower_tolerance_end < input_angle_value <= lower_tolerance_2:
                    actual_deviation = avg_value - input_angle_value
                    expected_deviation = avg_value - lower_tolerance_end
                    error = (actual_deviation / expected_deviation) * 100 if expected_deviation != 0 else 100
                    correct_percentage = max(0, 100 - error)
                else:
                    false_joints[angle_name] = input_angle_value, avg_value
                    print('Do Not Consider: ', angle_name)
                    continue

            if correct_percentage > 0:
                if status > 0:
                    considered_left_angles += 1
                    considered_high_std_angles_dict[angle_name] = input_angle_value
                elif status < 0:
                    considered_right_angles += 1
                    considered_low_std_angles_dict[angle_name] = input_angle_value
                else:
                    print('Error')

            correctness.append(correct_percentage)

    considered_angles = considered_left_angles + considered_right_angles
    overall_correctness = sum(correctness) / considered_angles if considered_angles > 0 else 0
    considered_joints_accuracy = round(overall_correctness)

    print('considered_high_std_angles_dict:', considered_high_std_angles_dict)
    print('considered_low_std_angles_dict:', considered_low_std_angles_dict)
    print('considered_angles:', considered_angles)
    print('sum of correctness:', sum(correctness))

    return considered_joints_accuracy

def calculate_accuracy(shot_type, input_angles):
    
    stats_files_for_batting_shots = {
        'forward defence': 'forward_defence_3dstats.csv',
        'forward drive': 'forward_drive_3dstats.csv',
        'backfoot defence': 'backfoot_defence_3dstats.csv',
        'backfoot drive': 'backfoot_drive_3dstats.csv'
    }

    if shot_type not in stats_files_for_batting_shots:
        raise ValueError(f"Unknown batting shot: {shot_type}")
    
    stats_file = f'{stats_directory}/{stats_files_for_batting_shots[shot_type]}'
    stats_data = pd.read_csv(stats_file)

    tolerances = calculate_tolerance_ranges(stats_data)
    average_angle_status = check_angle_upper_lower_status(input_angles, stats_data)

    percentage_error = calculate_percentage_accuracy(average_angle_status, tolerances, input_angles, stats_data)

    return percentage_error