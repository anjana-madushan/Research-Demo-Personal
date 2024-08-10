import joblib
from  Accuracy_calculations.accuracy_checker import calculate_accuracy

# load the classification model
clf = joblib.load(r'd:\\SLIIT\\Academic\\YEAR 04\\Research\\ModelTraining\\New-Re-trainedModel\\random_forest_classification.pkl')

# Load the MinMaxScaler
scaler = joblib.load(r'D:\\SLIIT\\Academic\\YEAR 04\\Research\\ModelTraining\\Newest_scalers\\min_max_scaler.pkl')


def predict(input_angles):
    # Receive features from the request
    features = input_angles.json['features']

    # Extract angle values from the features
    angle_values = [angle[1] for angle in features]

    # Preprocess the features
    features_normalized = scaler.transform([angle_values])

    # Predict using the classifier
    predicted_labels = clf.predict(features_normalized)
    confidence_levels = clf.predict_proba(features_normalized)

    # Get the confidence level for the predicted class
    predicted_class_confidence = max(confidence_levels[0])
    
    # Get the accuracy of the predicted shot
    results = calculate_accuracy(predicted_labels[0], features)

    output_data = {
        'predicted_labels': {'Performed shot is': predicted_labels[0]}, 'Accuracy checker':results,
        'Confidence Levels': {f"{shot_type}": confidence for shot_type, confidence in zip(clf.classes_, confidence_levels[0])},
        'Highest Confidence Level': predicted_class_confidence,
        'Accuracy checker': results
    }

    return output_data
