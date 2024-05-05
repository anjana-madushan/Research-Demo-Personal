import joblib

# load the classification model
clf = joblib.load(r'd:\SLIIT\Academic\YEAR 04\Research\ModelTraining\models\random_forest_classification.pkl')

# Load the MinMaxScaler
scaler = joblib.load(r'D:\SLIIT\Academic\YEAR 04\Research\ModelTraining\scalers\min_max_scaler.pkl')


def predict(input_angles):
    # Receive features from the request
    features = input_angles.json['features']

    # Extract angle values from the features
    angle_values = [angle[1] for angle in features]

    # Preprocess the features
    features_normalized = scaler.transform([angle_values])

    # Predict using the classifier
    predicted_labels = clf.predict(features_normalized)

    # output_data = {
    #     'input_angles': features,  # Only include the features
    #     'predicted_labels': {'Performed a shot is': predicted_labels[0]}
    # }

    output_data = {
        'predicted_labels': {'Performed shot is': predicted_labels[0]}
    }

    return output_data
