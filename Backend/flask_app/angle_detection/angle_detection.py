import os
import cv2
import mediapipe as mp
import numpy as np

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

import cv2
import mediapipe as mp
import numpy as np

def extract_angles(image_path):
    mp_pose = mp.solutions.pose

    # Load and preprocess image
    image = cv2.imread(image_path)
    preprocessed_image = preprocess_image(image)

    with mp_pose.Pose(static_image_mode=True, model_complexity=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Convert the BGR image to RGB before processing
        image_rgb = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)
        
        # Process preprocessed image
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Extract keypoints for relevant joints (including depth, i.e., z-coordinate)
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

            # Calculate angles (in degrees) using 3D coordinates
            def calculate_angle_3d(a, b, c):
                ab = a - b
                cb = c - b
                cosine_angle = np.dot(ab, cb) / (np.linalg.norm(ab) * np.linalg.norm(cb))
                angle = np.degrees(np.arccos(cosine_angle))
                return angle

            angle_left_elbow = calculate_angle_3d(left_shoulder, left_elbow, left_wrist)
            angle_right_elbow = calculate_angle_3d(right_shoulder, right_elbow, right_wrist)

            angle_left_shoulder = calculate_angle_3d(left_hip, left_shoulder, left_elbow)
            angle_right_shoulder = calculate_angle_3d(right_hip, right_shoulder, right_elbow)

            angle_left_knee = calculate_angle_3d(left_ankle, left_knee, left_hip)
            angle_right_knee = calculate_angle_3d(right_ankle, right_knee, right_hip)

            angle_left_hip = calculate_angle_3d(left_shoulder, left_hip, left_knee)
            angle_right_hip = calculate_angle_3d(right_shoulder, right_hip, right_knee)

            angle_left_hip_knee = calculate_angle_3d(right_hip, left_hip, left_knee)
            angle_right_hip_knee = calculate_angle_3d(left_hip, right_hip, right_knee)

            return [angle_left_elbow, angle_right_elbow, angle_left_shoulder, angle_right_shoulder,
                    angle_left_knee, angle_right_knee, angle_left_hip, angle_right_hip,
                    angle_left_hip_knee, angle_right_hip_knee]
        else:
            return None


# Function to extract keypoints and calculate angles from poses
# def extract_angles(image_path):
#     mp_pose = mp.solutions.pose

#     # Load and preprocess image
#     image = cv2.imread(image_path)
#     preprocessed_image = preprocess_image(image)

#     with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         # Convert the BGR image to RGB before processing
#         image_rgb = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)
        
#         # Process preprocessed image
#         results = pose.process(image_rgb)

#         if results.pose_landmarks:
#             landmarks = results.pose_landmarks.landmark

#             # Extract keypoints for relevant joints
#             left_shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
#                                       landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
#                                       landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z])
#             right_shoulder = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
#                                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
#                                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z])
#             left_elbow = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
#                                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
#                                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z])
#             right_elbow = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
#                                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
#                                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z])
#             left_hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
#                                  landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y,
#                                  landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z])
#             right_hip = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
#                                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y,
#                                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z])
#             left_wrist = np.array([landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
#                                   landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
#                                   landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z])
#             right_wrist = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
#                                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
#                                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z])
#             left_knee = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
#                                   landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y,
#                                   landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].z])
#             right_knee = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
#                                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
#                                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].z])
#             left_ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
#                                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y,
#                                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].z])
#             right_ankle = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
#                                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y,
#                                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].z])

#             # Calculate angles (in degrees)
#             angle_left_elbow = np.degrees(np.arccos(np.dot((left_shoulder - left_elbow), (left_wrist - left_elbow)) /
#                                              (np.linalg.norm(left_shoulder - left_elbow) *
#                                               np.linalg.norm(left_wrist - left_elbow))))
#             angle_right_elbow = np.degrees(np.arccos(np.dot((right_shoulder - right_elbow), (right_wrist - right_elbow)) /
#                                               (np.linalg.norm(right_shoulder - right_elbow) *
#                                                np.linalg.norm(right_wrist - right_elbow))))

#             angle_left_shoulder = np.degrees(np.arccos(np.dot((left_hip - left_shoulder), (left_elbow - left_shoulder)) /
#                                                (np.linalg.norm(left_hip - left_shoulder) *
#                                                 np.linalg.norm(left_elbow - left_shoulder))))
#             angle_right_shoulder = np.degrees(np.arccos(np.dot((right_hip - right_shoulder), (right_elbow - right_shoulder)) /
#                                                 (np.linalg.norm(right_hip - right_shoulder) *
#                                                  np.linalg.norm(right_elbow - right_shoulder))))

#             angle_left_knee = np.degrees(np.arccos(np.dot((left_ankle - left_knee), (left_hip - left_knee)) /
#                                             (np.linalg.norm(left_ankle - left_knee) *
#                                              np.linalg.norm(left_hip - left_knee))))
#             angle_right_knee = np.degrees(np.arccos(np.dot((right_ankle - right_knee), (right_hip - right_knee)) /
#                                              (np.linalg.norm(right_ankle - right_knee) *
#                                               np.linalg.norm(right_hip - right_knee))))

#             angle_left_hip = np.degrees(np.arccos(np.dot((left_shoulder - left_hip), (left_knee - left_hip)) /
#                                            (np.linalg.norm(left_shoulder - left_hip) *
#                                             np.linalg.norm(left_knee - left_hip))))
#             angle_right_hip = np.degrees(np.arccos(np.dot((right_shoulder - right_hip), (right_knee - right_hip)) /
#                                             (np.linalg.norm(right_shoulder - right_hip) *
#                                              np.linalg.norm(right_knee - right_hip))))

#             angle_left_hip_knee = np.degrees(np.arccos(np.dot((right_hip - left_hip), (left_knee - left_hip)) /
#                                                 (np.linalg.norm(right_hip - left_hip) *
#                                                  np.linalg.norm(left_knee - left_hip))))
#             angle_right_hip_knee = np.degrees(np.arccos(np.dot((left_hip - right_hip), (right_knee - right_hip)) /
#                                                  (np.linalg.norm(left_hip - right_hip) *
#                                                   np.linalg.norm(right_knee - right_hip))))

#             return [angle_left_elbow, angle_right_elbow, angle_left_shoulder, angle_right_shoulder,angle_left_knee, angle_right_knee, 
#                     angle_left_hip, angle_right_hip, angle_left_hip_knee, angle_right_hip_knee]
#         else:
#             return None