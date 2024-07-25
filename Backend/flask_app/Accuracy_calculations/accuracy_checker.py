import pandas as pd

stats_directory = 'D:/SLIIT/Academic/YEAR 04/Research/ModelTraining/stats'

def calculate_tolerance_ranges(stats_data):
    
    tolerances = pd.DataFrame(index=stats_data.index)
    tolerances['Angle'] = stats_data['Angle']
    tolerances['Upper_tolerance'] = abs(stats_data['Average'] +  (stats_data['Standard Deviation (Above Average)']))
    tolerances['lower_tolerance'] = abs(stats_data['Average'] - (stats_data['Standard Deviation (Below Average)']))
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
    correct_percentage = 0
    error = 0
    use_upper_tolerance = 0
    use_lower_tolerance = 0
    actual_deviation = 0
    
    for angle_name, input_angle_value in input_angles:
        if angle_name in average_angle_status['Angle'].values:
            status = average_angle_status.loc[average_angle_status['Angle'] == angle_name, 'Status'].values[0]
            avg_value = shot_stats.loc[shot_stats['Angle'] == angle_name, 'Average'].values[0]

            if status > 0:
                use_upper_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'Upper_tolerance'].values[0]
                actual_deviation = input_angle_value - avg_value
                expected_deviation = use_upper_tolerance - avg_value
                error = (actual_deviation/expected_deviation)*100
                if error<100:
                  correct_percentage = 100 - error
                elif error>100:
                  correct_percentage = 0
                  continue
                print("error with angle", actual_deviation/expected_deviation, correct_percentage, status, angle_name)
           
            elif status < 0:
                use_lower_tolerance = tolerances.loc[tolerances['Angle'] == angle_name, 'lower_tolerance'].values[0]
                actual_deviation = avg_value - input_angle_value
                expected_deviation = avg_value - use_lower_tolerance
                error = (actual_deviation/use_lower_tolerance)*100
                if error<100:
                  correct_percentage = 100 - error
                elif error>100:
                  correct_percentage = 0
                  continue
                print("error with angle", actual_deviation/use_lower_tolerance, correct_percentage, status, angle_name)
            correctness.append(correct_percentage)
            print('errors sum process', sum(correctness))
                
    overall_correctness = sum(correctness) / len(input_angles)
    print(len(input_angles))
    print('sum of correctness', sum(correctness))
    accuracy = round(overall_correctness) 
    return accuracy

def calculate_accuracy(shot_type, input_angles):
    
    print(input_angles)
    
    stats_files_for_batting_shots = {
        'forward defence': 'forward_defence_stats.csv',
        'forward drive': 'forward_drive_stats.csv',
        'backfoot defence': 'backfoot_defence_stats.csv',
        'backfoot drive': 'backfoot_drive_stats.csv'
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