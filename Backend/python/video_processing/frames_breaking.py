from flask import Flask, request, jsonify # type: ignore
import cv2
import os
import numpy as np
import mediapipe as mp
import pandas as pd
import sys
import os
import joblib

app = Flask(__name__)

clf = joblib.load(r'd:\SLIIT\Academic\YEAR 04\Research\ModelTraining\models\random_forest_classification.pkl')
print(clf)

# Load the MinMaxScaler
scaler = joblib.load(r'D:\SLIIT\Academic\YEAR 04\Research\ModelTraining\scalers\min_max_scaler.pkl')
print(scaler)

# Function to preprocess images
def preprocess_image(image):
    # Apply Gaussian Blur to remove blur
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Apply Median Blur to remove salt-and-pepper noise
    median_blurred_image = cv2.medianBlur(blurred_image, 5)
    
    # Perform resizing and cropping if necessary
    resized_image = cv2.resize(median_blurred_image, (224, 224))
    
    # Normalize pixel values to range [0, 1]
    normalized_image = resized_image / 255.0
    
    # Convert image to 8-bit unsigned integer depth
    uint8_image = (normalized_image * 255).astype(np.uint8)
    
    return uint8_image

# Function to extract keypoints and calculate angles from poses
def extract_angles(image_np):
    mp_pose = mp.solutions.pose

    preprocessed_image = preprocess_image(image_np)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Convert the BGR image to RGB before processing
        image_rgb = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)
        
        # Process preprocessed image
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Extract keypoints for relevant joints
            left_shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z])
            right_shoulder = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                       landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                                       landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z])
            left_elbow = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z])
            right_elbow = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z])
            left_hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y,
                                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z])
            right_hip = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z])
            left_wrist = np.array([landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
                                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z])
            right_wrist = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z])
            left_knee = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y,
                                  landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].z])
            right_knee = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].z])
            left_ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].z])
            right_ankle = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].z])

            # Calculate angles (in degrees)
            angle_left_elbow = np.degrees(np.arccos(np.dot((left_shoulder - left_elbow), (left_wrist - left_elbow)) /
                                             (np.linalg.norm(left_shoulder - left_elbow) *
                                              np.linalg.norm(left_wrist - left_elbow))))
            angle_right_elbow = np.degrees(np.arccos(np.dot((right_shoulder - right_elbow), (right_wrist - right_elbow)) /
                                              (np.linalg.norm(right_shoulder - right_elbow) *
                                               np.linalg.norm(right_wrist - right_elbow))))

            angle_left_shoulder = np.degrees(np.arccos(np.dot((left_hip - left_shoulder), (left_elbow - left_shoulder)) /
                                               (np.linalg.norm(left_hip - left_shoulder) *
                                                np.linalg.norm(left_elbow - left_shoulder))))
            angle_right_shoulder = np.degrees(np.arccos(np.dot((right_hip - right_shoulder), (right_elbow - right_shoulder)) /
                                                (np.linalg.norm(right_hip - right_shoulder) *
                                                 np.linalg.norm(right_elbow - right_shoulder))))

            angle_left_knee = np.degrees(np.arccos(np.dot((left_ankle - left_knee), (left_hip - left_knee)) /
                                            (np.linalg.norm(left_ankle - left_knee) *
                                             np.linalg.norm(left_hip - left_knee))))
            angle_right_knee = np.degrees(np.arccos(np.dot((right_ankle - right_knee), (right_hip - right_knee)) /
                                             (np.linalg.norm(right_ankle - right_knee) *
                                              np.linalg.norm(right_hip - right_knee))))

            angle_left_hip = np.degrees(np.arccos(np.dot((left_shoulder - left_hip), (left_knee - left_hip)) /
                                           (np.linalg.norm(left_shoulder - left_hip) *
                                            np.linalg.norm(left_knee - left_hip))))
            angle_right_hip = np.degrees(np.arccos(np.dot((right_shoulder - right_hip), (right_knee - right_hip)) /
                                            (np.linalg.norm(right_shoulder - right_hip) *
                                             np.linalg.norm(right_knee - right_hip))))

            angle_left_hip_knee = np.degrees(np.arccos(np.dot((right_hip - left_hip), (left_knee - left_hip)) /
                                                (np.linalg.norm(right_hip - left_hip) *
                                                 np.linalg.norm(left_knee - left_hip))))
            angle_right_hip_knee = np.degrees(np.arccos(np.dot((left_hip - right_hip), (right_knee - right_hip)) /
                                                 (np.linalg.norm(left_hip - right_hip) *
                                                  np.linalg.norm(right_knee - right_hip))))

            return [angle_left_elbow, angle_right_elbow, angle_left_shoulder, angle_right_shoulder,angle_left_knee, angle_right_knee, 
                    angle_left_hip, angle_right_hip, angle_left_hip_knee, angle_right_hip_knee]
        else:
            return None

# def video_to_frames(video_path, output_dir, frame_skip):
#     # Create output directory if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)
    
#     print(video_path);
#     # Open the video file
#     cap = cv2.VideoCapture(video_path)
#     frame_count = 0
    
#     # Read frames from the video
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         # Save the frame as an image file
#         if frame_count % frame_skip == 0:
#             frame_path = os.path.join(output_dir, f'frame_{frame_count}.jpg')
#             cv2.imwrite(frame_path, frame)
        
#             print(frame_count);
#         frame_count += 1
    
#     # Release the VideoCapture
#     cap.release()

# @app.route('/process_video', methods=['POST'])
# def process_video():
#     data = request.json
#     print(data);
#     video_path = data['videoPath']
#     output_dir = data['outputDir']
#     frame_skip = data['frameSkip']

#     video_path = f'D:\SLIIT\Academic\YEAR 04\Research\PP1\Research-Demo-Personal\Backend\server\{video_path}'

#     video_to_frames(video_path, output_dir, frame_skip)

#     return jsonify({'message': 'Video processing completed'})

@app.route('/process_image', methods=['POST'])
def extract_angles_endpoint():
    # Check if an image file is present in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Read the image file from the request
    image_file = request.files['image']

    # Check if the file is empty
    if image_file.filename == '':
        return jsonify({'error': 'Empty file provided'}), 400

    # Read the image as a numpy array
    image_bytes = image_file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Extract angles from the image
    angles = extract_angles(image_np)

    if angles is not None:
        # Return the extracted angles as a JSON response
        return jsonify({'angles': angles}), 200
    else:
        return jsonify({'error': 'No poses detected in the image'}), 400

@app.route('/predict', methods=['POST'])
def predict():
    # Receive features from the request
    features = request.json['features']

    # Extract angle values from the features
    angle_values = [angle[1] for angle in features]

    # Preprocess the features
    features_normalized = scaler.transform([angle_values])

    # Predict using the classifier
    predicted_labels = clf.predict(features_normalized)

    # Return the predicted labels
    return jsonify({'Performed a shot is': predicted_labels[0]})

if __name__ == '__main__': 
    app.run(debug=True)  # Run the Flask app
