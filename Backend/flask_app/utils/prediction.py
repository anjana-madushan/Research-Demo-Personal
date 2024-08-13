import joblib
import pandas as pd
from Accuracy_calculations.accuracy_checker import calculate_accuracy
from utils.extract_angles import extract_angles

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
        angles = extract_angles(image_np)
        mae_value, rectification_messages = calculate_accuracy(predicted_labels[0], angles)
        print(mae_value, rectification_messages)

        if predicted_class_confidence < 0.5:
            output_error = 'The pose is not recognizable'
            output_data = {
                'response': output_error,
                'Stroke': predicted_labels[0],  # Changed from set to list
                # 'Confidence Levels': {shot_type: confidence for shot_type, confidence in zip(clf.classes_, confidence_levels[0])},
                # 'Highest Confidence Level': predicted_class_confidence
            }
        else:
            output_data = {
                'accuracy':f'{mae_value}%',
                'rectifications':rectification_messages,
                'Stroke': predicted_labels[0],
                # 'Confidence Levels': {shot_type: confidence for shot_type, confidence in zip(clf.classes_, confidence_levels[0])},
                # 'Highest Confidence Level': predicted_class_confidence
            }

    except Exception as e:
        output_data = {
            'error': str(e)
        }

    return output_data
