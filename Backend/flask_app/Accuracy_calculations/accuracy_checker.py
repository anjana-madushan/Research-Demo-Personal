import pandas as pd

stats_directory = 'D:/SLIIT/Academic/YEAR 04/Research/ModelTraining/stats'

def calculate_tolerance_ranges(df):
    
    tolerances = pd.DataFrame(index=df.index)
    tolerances['Angle'] = df['Angle']
    tolerances['Upper_tolerance'] = abs(df['Average'] +  (df['Standard Deviation (Above Average)']))
    tolerances['lower_tolerance'] = abs(df['Average'] - (df['Standard Deviation (Below Average)']))
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
                # if(error<0):
                #         #actual deviation is higher than the expected deviation
                #     error = abs(error)
                #     errors.append(error)
                # elif(error>0):
                #     errors.append(error)
           
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
                # if(error<0):
                #     #actual deviation is higher than the expected deviation
                #     error = abs(error)
                #     errors.append(error)
                # elif(error>0):
                #     errors.append(error)
            correctness.append(correct_percentage)
            print('errors sum process', sum(correctness))
                
    overall_correctness = sum(correctness) / len(input_angles)
    print(len(input_angles))
    print('sum of correctness', sum(correctness))
    accuracy = round(overall_correctness) 
    return accuracy

def calculate_accuracy(shotType, input_angles):
    
    print(input_angles)
    forward_drive_stats = pd.read_csv(f'{stats_directory}/forward_drive_stats.csv')

    tolerances = 0
    
    if shotType == 'forward defence':
        forward_defence_stats = pd.read_csv(f'{stats_directory}/forward_defence_stats.csv')
        tolerances = calculate_tolerance_ranges(forward_defence_stats)
        print('fde',tolerances)
    elif shotType == 'forward drive':
        print(forward_drive_stats)
        tolerances = calculate_tolerance_ranges(forward_drive_stats)
        print(tolerances)
    elif shotType == 'backfoot defence':
        backfoot_defence_stats = pd.read_csv(f'{stats_directory}/backfoot_defence_stats.csv')
        tolerances = calculate_tolerance_ranges(backfoot_defence_stats)
        print('bd',tolerances)
    elif shotType == 'backfoot drive':
        backfoot_drive_stats = pd.read_csv(f'{stats_directory}/backfoot_drive_stats.csv')
        tolerances = calculate_tolerance_ranges(backfoot_drive_stats)
        print('bdr',tolerances)

    average_angle_status = check_angle_upper_lower_status(input_angles, forward_drive_stats)
    print(average_angle_status)

    percentage_error = calculate_percentage_accuracy(average_angle_status, tolerances, input_angles, forward_drive_stats)

    return percentage_error