import joblib
import pandas as pd
from Accuracy_calculations.accuracy_checker import calculate_accuracy

# Load the classification model
clf = joblib.load(r'd:\\SLIIT\\Academic\\YEAR 04\\Research\\ModelTraining\\Aug4-trainedModel\\random_forest_classification.pkl')

# Load the MinMaxScaler if needed
# scaler = joblib.load(r'D:\\SLIIT\\Academic\\YEAR 04\\Research\\ModelTraining\\Newest_scalers\\min_max_scaler.pkl')

def predict(features):
    try:
        # Convert the dictionary into a DataFrame with a single row
        df = pd.DataFrame([features])
        output_error = {}

        # Predict using the classifier
        predicted_labels = clf.predict(df)
        confidence_levels = clf.predict_proba(df)

        # Get the confidence level for the predicted class
        predicted_class_confidence = max(confidence_levels[0])

        if predicted_class_confidence < 0.5:
            output_error = 'The pose is not recognizable'
            output_data = {
                'response': output_error,
                'Shot you are trying': [predicted_labels[0]],  # Changed from set to list
                'Confidence Levels': {shot_type: confidence for shot_type, confidence in zip(clf.classes_, confidence_levels[0])},
                'Highest Confidence Level': predicted_class_confidence
            }
        else:
            output_data = {
                'predicted_labels': [f'Performed shot is {predicted_labels[0]}'],  # Changed from set to list
                'Confidence Levels': {shot_type: confidence for shot_type, confidence in zip(clf.classes_, confidence_levels[0])},
                'Highest Confidence Level': predicted_class_confidence
            }

    except Exception as e:
        output_data = {
            'error': str(e)
        }

    return output_data
