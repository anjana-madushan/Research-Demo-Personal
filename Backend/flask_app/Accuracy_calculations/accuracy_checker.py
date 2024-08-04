import pandas as pd

stats_directory = 'D:/SLIIT/Academic/YEAR 04/Research/ModelTraining/newStats'

def calculate_tolerance_ranges(stats_data):
    
    tolerances = pd.DataFrame(index=stats_data.index)
    tolerances['Angle'] = stats_data['Angle']
    tolerances['Upper_tolerance'] = abs(stats_data['Average'] +  (stats_data['Standard Deviation (Above Average)'])*2)
    tolerances['lower_tolerance'] = abs(stats_data['Average'] - (stats_data['Standard Deviation (Below Average)'])*2)
    print(tolerances)
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

    for angle_name, input_angle_value in input_angles:
        if angle_name in average_angle_status['Angle'].values:
            status = average_angle_status.loc[average_angle_status['Angle'] == angle_name, 'Status'].values[0]
            avg_value = shot_stats.loc[shot_stats['Angle'] == angle_name, 'Average'].values[0]

            if status > 0:
                upper_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'Upper_tolerance'].values[0]
                actual_deviation = input_angle_value - avg_value
                expected_deviation = upper_tolerance - avg_value
            else:
                lower_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'lower_tolerance'].values[0]
                actual_deviation = avg_value - input_angle_value
                expected_deviation = avg_value - lower_tolerance

            error = (actual_deviation / expected_deviation) * 100
            correct_percentage = max(0, 100 - error)

            if correct_percentage > 0:
                if status > 0:
                    considered_left_angles += 1
                    considered_high_std_angles_dict[angle_name] = input_angle_value
                else:
                    considered_right_angles += 1
                    considered_low_std_angles_dict[angle_name] = input_angle_value
            else:
                if status > 0:
                    totally_wrong_high_std_angles_dict[angle_name] = input_angle_value
                else:
                    totally_wrong_low_std_angles_dict[angle_name] = input_angle_value

            correctness.append(correct_percentage)

    considered_angles = considered_left_angles + considered_right_angles
    overall_correctness = sum(correctness) / considered_angles if considered_angles > 0 else 0
    accuracy = round(overall_correctness)

    print('considered_high_std_angles_dict:', considered_high_std_angles_dict)
    print('totally_wrong_high_std_angles_dict:', totally_wrong_high_std_angles_dict)
    print('considered_low_std_angles_dict:', considered_low_std_angles_dict)
    print('totally_wrong_low_std_angles_dict:', totally_wrong_low_std_angles_dict)
    print('considered_angles:', considered_angles)
    print('sum of correctness:', sum(correctness))

    return accuracy

def calculate_accuracy(shot_type, input_angles):
    
    print(input_angles)
    
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

    print(average_angle_status)

    percentage_error = calculate_percentage_accuracy(average_angle_status, tolerances, input_angles, stats_data)

    return percentage_error