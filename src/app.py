from flask import Flask, request, jsonify, send_from_directory, Response,send_file
from flask_cors import CORS
import os
import subprocess
import glob

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def run_inference(file_path):
    # Run YOLOv5 inference using detect.py script
    output_dir = 'output'
    print('file path: ',file_path)
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    output_path = os.path.join(output_dir, 'temp.jpg')  # Use 'temp.jpg' as the file name
    print('output path:',output_path)
    command = [
        "python",
        r"C:\Users\torjm\OneDrive\Bureau\Tunisian Traffic sign\my-app\models\yolov5\detect.py",
        "--weights",
        r"C:\Users\torjm\OneDrive\Bureau\Tunisian Traffic sign\my-app\models\best.pt",
        "--img-size",
        "640",
        "--conf",
        "0.5",  # Set confidence threshold as needed
        "--source",
        file_path,
        "--save-txt",
        "--save-conf",
        "--exist-ok",
        "--project",
        output_dir,
        "--name",
        "result"
    ]

    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        print('Inference completed successfully')
        return output_path
    except subprocess.CalledProcessError as e:
        print('Error during inference:', e)
        return {"error": str(e)}

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle file upload
    file = request.files['file']

    # Save the file to a temporary location
    save_dir = 'uploads'
    os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(save_dir, 'temp.jpg')
    file.save(file_path)
    result_image_path = run_inference(file_path)
    return jsonify({'message': 'File uploaded successfully', 'result_image_path': result_image_path})

@app.route('/output/result/<filename>')
def result_image(filename):
    return send_from_directory(os.path.abspath('output/result'), filename, mimetype='image/jpeg')

@app.route('/output/result/<filename>')
def uploaded_file(filename):
    return send_from_directory('output/result', filename)

if __name__ == '__main__':
    app.run(debug=True)
