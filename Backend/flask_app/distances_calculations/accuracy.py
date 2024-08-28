import numpy as np
import mediapipe as mp
import cv2

def calculate_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

def extract_accuracy_distances(image_np):
    mp_pose = mp.solutions.pose
    
    with mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False, min_detection_confidence=0.2) as pose:
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        if results.pose_world_landmarks:
            landmarks = results.pose_world_landmarks.landmark
            
            # Extract keypoints
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
                'RIGHT_WRIST': np.array([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
                                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z]),
            }

            distances = {              
                'left_shoulder_right_shoulder': calculate_distance(points['LEFT_SHOULDER'], points['RIGHT_SHOULDER']),
                'right_shoulder_right_elbow': calculate_distance(points['RIGHT_SHOULDER'], points['RIGHT_ELBOW']),
                'right_shoulder_right_hip': calculate_distance(points['RIGHT_SHOULDER'], points['RIGHT_HIP']),
                'left_hip_right_hip': calculate_distance(points['LEFT_HIP'], points['RIGHT_HIP']),
                'right_hip_right_knee': calculate_distance(points['RIGHT_HIP'], points['RIGHT_KNEE']),
                'right_knee_right_ankle': calculate_distance(points['RIGHT_KNEE'], points['RIGHT_ANKLE']),
            }
            
            
            return distances
        else:
            return None