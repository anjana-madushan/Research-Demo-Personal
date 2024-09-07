from flask import Flask, request, jsonify # type: ignore
import numpy as np
import cv2
from flask_cors import CORS

from distances_calculations.classification import extract_distances
from utils.prediction import predict

app = Flask(__name__)
CORS(app)

def process_image_data(image_bytes, batsman_type):
    
    # Convert the image bytes to a numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    
    # Convert numpy array into an OpenCV image
    image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Extract distances between landmarks 
    distances = extract_distances(image_np, batsman_type)

    # Check if distances were extracted successfully
    if distances is None:
        return None, "No poses detected in the image"

    # Use extracted distances to do classification, 
    # accuracy calculations and provide rectifications
    predicted_stroke_data = predict(distances, image_np, batsman_type)
    
    return predicted_stroke_data

@app.route('/api/upload/image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    # print(request.form['type'])
    image_file = request.files['image']
    batsman_type = request.form['type']
    
    if 'type' not in request.form:
        return jsonify({"error": "Enter the batsman type"}), 400

    if image_file.filename == '':
        return jsonify({"error": "No image selected"}), 400
    
    try:
        # Read the image file directly from the request
        image_bytes = image_file.read()

        # Process the image
        output_data = process_image_data(image_bytes, batsman_type)
        
        # Return the result
        return jsonify(output_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__': 
    app.run(debug=True)  