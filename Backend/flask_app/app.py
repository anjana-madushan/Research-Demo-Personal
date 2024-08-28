from flask import Flask, request, jsonify # type: ignore
import numpy as np
import cv2

from distances_calculations.classification import extract_distances
from utils.prediction import predict

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def extract_angles_endpoint():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'Empty file provided'}), 400

    image_bytes = image_file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    distances = extract_distances(image_np)

    if distances is not None:
        output_data = predict(distances, image_np)
        return jsonify(output_data)
    else:
        return jsonify({'error': 'No poses detected in the image'}), 400

if __name__ == '__main__': 
    app.run(debug=True)  

# @app.route('/process_image', methods=['POST'])
# def extract_angles_endpoint():
#     # Check if an image file is present in the request
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400

#     # Read the image file from the request
#     image_file = request.files['image']

#     # Check if the file is empty
#     if image_file.filename == '':
#         return jsonify({'error': 'Empty file provided'}), 400

#     # Read the image as a numpy array
#     image_bytes = image_file.read()
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Extract angles from the image using extract_angle util function
#     # angles = extract_angles(image_np)
#     distance = extract_distances(image_np)

#     if distance is not None:
#         # Return the extracted angles as a JSON response
#         finalized_distance = jsonify({'features': distance})
#         print(distance)
#         return predict(finalized_distance)
#     else:
#         return jsonify({'error': 'No poses detected in the image'}), 400

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

# Run the Flask app