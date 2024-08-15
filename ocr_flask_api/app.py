from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
from io import BytesIO

app = Flask(__name__)

# Set the path to the Tesseract executable (modify the path as needed)
pytesseract.pytesseract.tesseract_cmd = r'E:\tesseract\tesseract.exe'

# Endpoint to fetch and process captcha image from URL
@app.route('/api/get_captcha_value', methods=['POST'])
def get_captcha_value():
    if 'captcha_image' not in request.files:
        return jsonify({'error': 'No captcha image provided'}), 400

    captcha_image = request.files['captcha_image']
    print('Received image:', captcha_image.filename)  # Debugging: Print filename

    # Open image from file storage
    try:
        img = Image.open(captcha_image)
    except Exception as e:
        return jsonify({'error': f'Failed to open captcha image: {str(e)}'}), 400

    # Use pytesseract to extract text from image
    try:
        captcha_text = pytesseract.image_to_string(img, lang='eng')  # Adjust language as needed
        print('Extracted text:', captcha_text)  # Debugging: Print extracted text
    except pytesseract.TesseractNotFoundError:
        return jsonify({'error': 'Tesseract OCR is not installed or not found'}), 500
    except Exception as e:
        return jsonify({'error': f'OCR processing error: {str(e)}'}), 500

    return jsonify({'captcha_value': captcha_text.strip()}), 200

if __name__ == '__main__':
    app.run(debug=True)
