import numpy as np
import mediapipe as mp
import cv2

from utils.shank_calculations.shankAngleCalculate import shankAngleCalculate
from utils.shank_calculations.shankAngleProcess import shankAngleCalculationProcess

def calculate_angle(A, B, C):
    AB = A - B
    CB = C - B
    dot_product = np.dot(AB, CB)
    magnitude_AB = np.linalg.norm(AB)
    magnitude_CB = np.linalg.norm(CB)
    cosine_angle = dot_product / (magnitude_AB * magnitude_CB)
    angle = np.degrees(np.arccos(cosine_angle))
    return round(angle, 3)

def extract_angles(image_np):
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
            
            # Calculate angles
            angles = {
                'angle_right_elbow': calculate_angle(points['RIGHT_SHOULDER'], points['RIGHT_ELBOW'], points['RIGHT_WRIST']),
                'angle_left_elbow': calculate_angle(points['LEFT_SHOULDER'], points['LEFT_ELBOW'], points['RIGHT_WRIST']),
                'angle_right_shoulder': calculate_angle(points['RIGHT_HIP'], points['RIGHT_SHOULDER'], points['RIGHT_ELBOW']),
                'angle_left_knee': calculate_angle(points['LEFT_HIP'], points['LEFT_KNEE'], points['LEFT_ANKLE']),
                'angle_right_knee': calculate_angle(points['RIGHT_HIP'], points['RIGHT_KNEE'], points['RIGHT_ANKLE']),
                'angle_right_hip_knee':calculate_angle(points['RIGHT_KNEE'], points['RIGHT_HIP'], points['LEFT_HIP']),
                'angle_left_hip_knee':calculate_angle(points['LEFT_KNEE'], points['LEFT_HIP'], points['RIGHT_HIP']),
                'angle_right_hip_shoulder': calculate_angle(points['RIGHT_KNEE'], points['RIGHT_HIP'], points['RIGHT_SHOULDER']),
                'angle_right_shank':shankAngleCalculationProcess(points['RIGHT_ANKLE'], points['RIGHT_KNEE'], points['LEFT_ANKLE']),
                'angle_left_shank':shankAngleCalculationProcess(points['LEFT_ANKLE'], points['LEFT_KNEE'], points['RIGHT_ANKLE']),
            }
            
            return angles
        else:
            # with open(log_file, 'a') as log:
            #     log.write(f"No landmarks detected in image: {os.path.basename(image_path)}\n")
            return None
