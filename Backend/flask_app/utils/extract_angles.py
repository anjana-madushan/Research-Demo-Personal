import numpy as np
import mediapipe as mp
import cv2
from utils.shank_calculations.shankAngleProcess import shankAngleCalculationProcess
from utils.preprocessing import preprocess_image

def calculate_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

def extract_distances(image_np):
    mp_pose = mp.solutions.pose
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    
    with mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False, min_detection_confidence=0.2) as pose:
        results = pose.process(image_rgb)
        
        if results.pose_world_landmarks:
            landmarks = results.pose_world_landmarks.landmark
            
            # Extract only the required keypoints
            points = {
                'LEFT_SHOULDER': np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                           landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                                           landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]),
                'RIGHT_SHOULDER': np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]),
                'LEFT_ELBOW': np.array([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
                                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]),
                'RIGHT_ELBOW': np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
                                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z]),
                'LEFT_HIP': np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                      landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y,
                                      landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z]),
                'RIGHT_HIP': np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y,
                                       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z]),
                'LEFT_KNEE': np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                       landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y,
                                       landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].z]),
                'RIGHT_KNEE': np.array([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
                                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].z]),
                'LEFT_ANKLE': np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                        landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y,
                                        landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].z]),
                'RIGHT_ANKLE': np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                         landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y,
                                         landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].z]),
                'NOSE':np.array([landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                                 landmarks[mp_pose.PoseLandmark.NOSE.value].y,
                                 landmarks[mp_pose.PoseLandmark.NOSE.value].z])
            }
            
            # Compute distances between keypoints
            distances = {
                # 'left_shoulder_right_shoulder': calculate_distance(points['LEFT_SHOULDER'], points['RIGHT_SHOULDER']),
                # 'left_shoulder_left_elbow': calculate_distance(points['LEFT_SHOULDER'], points['LEFT_ELBOW']),
                # 'right_shoulder_right_elbow': calculate_distance(points['RIGHT_SHOULDER'], points['RIGHT_ELBOW']),
                # 'left_hip_right_hip': calculate_distance(points['LEFT_HIP'], points['RIGHT_HIP']),
                # 'left_knee_right_knee': calculate_distance(points['LEFT_KNEE'], points['RIGHT_KNEE']),
                # 'left_ankle_right_ankle': calculate_distance(points['LEFT_ANKLE'], points['RIGHT_ANKLE']),
                # 'left_knee_right_elbow':calculate_distance(points['LEFT_KNEE'], points['RIGHT_ELBOW']),
                # 'right_shoulder_left_knee':calculate_distance(points['RIGHT_SHOULDER'], points['LEFT_KNEE']),
                # 'right_hip_left_ankle':calculate_distance(points['RIGHT_HIP'], points['LEFT_ANKLE']),
                # 'right_knee_left_ankle':calculate_distance(points['RIGHT_KNEE'], points['LEFT_ANKLE']),
                # 'left_knee_right_ankle':calculate_distance(points['LEFT_KNEE'], points['RIGHT_ANKLE']),
                # 'nose_left_knee':calculate_distance(points['NOSE'], points['LEFT_KNEE']),
                # 'nose_left_ankle': calculate_distance(points['NOSE'], points['LEFT_ANKLE'])
                # 'nose_left_shoulder': calculate_distance(points['NOSE'], points['LEFT_SHOULDER']),
                'nose_right_shoulder': calculate_distance(points['NOSE'], points['RIGHT_SHOULDER']),
                'nose_left_elbow': calculate_distance(points['NOSE'], points['LEFT_ELBOW']),
                'nose_right_elbow': calculate_distance(points['NOSE'], points['RIGHT_ELBOW']),
                # 'nose_left_hip': calculate_distance(points['NOSE'], points['LEFT_HIP']),
                # 'nose_right_hip': calculate_distance(points['NOSE'], points['RIGHT_HIP']),
                'nose_left_knee': calculate_distance(points['NOSE'], points['LEFT_KNEE']),
                'nose_right_knee': calculate_distance(points['NOSE'], points['RIGHT_KNEE']),
                'nose_left_ankle': calculate_distance(points['NOSE'], points['LEFT_ANKLE']),
                'nose_right_ankle': calculate_distance(points['NOSE'], points['RIGHT_ANKLE']),
                'left_knee_right_knee':calculate_distance(points['LEFT_KNEE'], points['RIGHT_KNEE']),
                'left_ankle_right_ankle':calculate_distance(points['LEFT_ANKLE'], points['RIGHT_ANKLE']),
                'left_shoulder_right_elbow':calculate_distance(points['LEFT_SHOULDER'], points['RIGHT_ELBOW']),
                'right_shoulder_left_elbow':calculate_distance(points['RIGHT_SHOULDER'], points['LEFT_ELBOW']),
            }
            return distances
        else:
            return None

def extract_angles(image_np):
    mp_pose = mp.solutions.pose

    preprocessed_image = preprocess_image(image_np)

    with mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False, min_detection_confidence=0.5) as pose:
        # Convert the BGR image to RGB before processing
        image_rgb = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)
        
        # Process preprocessed image
        results = pose.process(image_rgb)

        angle_names = [
        "angle_left_elbow",
        "angle_right_elbow",
        "angle_left_shoulder",
        "angle_right_shoulder",
        "angle_left_knee",
        "angle_right_knee",
        "angle_left_hip",
        "angle_right_hip",
        "angle_left_hip_knee",
        "angle_right_hip_knee",
        "right_shank_angle"
        ]

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
            
            right_shank_angle = shankAngleCalculationProcess(right_ankle, right_knee)

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
            
            angle_values = [angle_left_elbow, angle_right_elbow, angle_left_shoulder, angle_right_shoulder,angle_left_knee, angle_right_knee, 
                    angle_left_hip, angle_right_hip, angle_left_hip_knee, angle_right_hip_knee, right_shank_angle]
            
            features = [[angle_name, angle_value] for angle_name, angle_value in zip(angle_names, angle_values)]
            # print(features)

            return features
        else:
            return None