from flask import Flask, request, jsonify # type: ignore
import numpy as np
import cv2
from utils.extract_angles import extract_angles
from utils.prediction import predict

app = Flask(__name__)

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

    # Extract angles from the image using extract_angle util function
    angles = extract_angles(image_np)

    if angles is not None:
        # Return the extracted angles as a JSON response
        finalized_angles = jsonify({'features': angles})
        return predict(finalized_angles)
    else:
        return jsonify({'error': 'No poses detected in the image'}), 400

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
if __name__ == '__main__': 
    app.run(debug=True)  