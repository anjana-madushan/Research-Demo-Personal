import joblib
import pandas as pd
from Accuracy_calculations.accuracy_checker_updated import calculate_accuracy_and_mae
from Accuracy_calculations.similarity_finder import find_closest_match
from distances_calculations.accuracy import extract_accuracy_distances
from angle_calculations.extract_angles import extract_angles

# Load the classification model
clf = joblib.load(r'd:\\SLIIT\\Academic\\YEAR 04\\Research\\Training\\New-trainedModel\\random_forest_classification.pkl')

# Load the MinMaxScaler
scaler = joblib.load(r'D:\\SLIIT\\Academic\\YEAR 04\\Research\\ModelTraining\\New_scalers\\min_max_scaler.pkl')

def predict(features, image_np):
    try:
        # Convert the dictionary into a DataFrame with a single row
        df = pd.DataFrame([features])
        output_error = {}

        # Scale the features using the loaded MinMaxScaler
        scaled_features = scaler.transform(df)

        # Predict using the classifier with scaled features
        predicted_labels = clf.predict(scaled_features)
        confidence_levels = clf.predict_proba(scaled_features)

        # Get the confidence level for the predicted class
        predicted_class_confidence = max(confidence_levels[0])
        accuracy_distances = extract_accuracy_distances(image_np)
        closet_matches = find_closest_match(accuracy_distances, predicted_labels[0])

        angles = extract_angles(image_np)
        result = calculate_accuracy_and_mae(predicted_labels[0], angles, closet_matches)

        accuracy = result['Accuracy']
        rectifications = result['Rectification Messages']
        if predicted_class_confidence < 0.5:
            output_error = 'The pose is not recognizable'
            output_data = {
                'response': output_error,
                'Stroke': predicted_labels[0], 
                # 'Confidence Levels': {shot_type: confidence for shot_type, confidence in zip(clf.classes_, confidence_levels[0])},
                'Highest Confidence Level': predicted_class_confidence
            }
        else:
            output_data = {
                'accuracy':f'{accuracy}%',
                'rectifications':rectifications,
                'Stroke': predicted_labels[0],
                # 'Confidence Levels': {shot_type: confidence for shot_type, confidence in zip(clf.classes_, confidence_levels[0])},
                'Highest Confidence Level': predicted_class_confidence
            }

    except Exception as e:
        output_data = {
            'error': str(e)
        }

    return output_data
