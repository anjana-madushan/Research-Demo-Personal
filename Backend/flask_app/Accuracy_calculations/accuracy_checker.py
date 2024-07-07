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
    

def calculate_accuracy(shotType, input_angles):
    
    print('input_angles', input_angles)
    forward_drive_stats = pd.read_csv(f'{stats_directory}/forward_drive_stats.csv')
    
    if shotType == 'forward defence':
        forward_defence_stats = pd.read_csv(f'{stats_directory}/forward_defence_stats.csv')
        tolerances = calculate_tolerance_ranges(forward_defence_stats)
        print('fde',tolerances)
    elif shotType == 'forward drive':
        print(forward_drive_stats)
        tolerances = calculate_tolerance_ranges(forward_drive_stats)
    elif shotType == 'backfoot defence':
        backfoot_defence_stats = pd.read_csv(f'{stats_directory}/backfoot_defence_stats.csv')
        tolerances = calculate_tolerance_ranges(backfoot_defence_stats)
        print('bd',tolerances)
    elif shotType == 'backfoot drive':
        backfoot_drive_stats = pd.read_csv(f'{stats_directory}/backfoot_drive_stats.csv')
        tolerances = calculate_tolerance_ranges(backfoot_drive_stats)
        print('bdr',tolerances)

    average_angle_status = check_angle_upper_lower_status(input_angles, forward_drive_stats);
    print(average_angle_status)