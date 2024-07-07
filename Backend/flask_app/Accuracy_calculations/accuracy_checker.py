import pandas as pd

stats_directory = 'D:/SLIIT/Academic/YEAR 04/Research/ModelTraining/stats'

print('stats_directory', stats_directory);

backfoot_defence_stats = pd.read_csv(f'{stats_directory}/backfoot_defence_stats.csv')
backfoot_drive_stats = pd.read_csv(f'{stats_directory}/backfoot_drive_stats.csv')
forward_defence_stats = pd.read_csv(f'{stats_directory}/forward_defence_stats.csv')
forward_drive_stats = pd.read_csv(f'{stats_directory}/forward_drive_stats.csv')

def calculate_tolerance_ranges(df):
    
    tolerances = pd.DataFrame(index=df.index)
    tolerances['Angle'] = df['Angle']
    tolerances['Upper_tolerance'] = abs(df['Average'] +  (df['Standard Deviation (Above Average)']))
    tolerances['lower_tolerance'] = abs(df['Average'] - (df['Standard Deviation (Below Average)']))
    return tolerances

def calculate_accuracy(shotType, input_angles):
    
    print('input_angles', input_angles)
    
    if shotType == 'forward defence':
        tolerances = calculate_tolerance_ranges(forward_defence_stats)
        print('fde',tolerances)
    elif shotType == 'forward drive':
        print(forward_drive_stats)
        tolerances = calculate_tolerance_ranges(forward_drive_stats)
        print('fdr', tolerances)
    elif shotType == 'backfoot defence':
        tolerances = calculate_tolerance_ranges(backfoot_defence_stats)
        print('bd',tolerances)
    elif shotType == 'backfoot drive':
        tolerances = calculate_tolerance_ranges(backfoot_drive_stats)
        print('bdr',tolerances)