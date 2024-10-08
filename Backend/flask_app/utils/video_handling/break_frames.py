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