import sys
import logging
from flask import Flask, jsonify, render_template, request
from ocr import process_image

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JSON_AS_ASCII'] = False
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


@app.errorhandler(404)
def not_found(error):
	resp = jsonify({'error': 'Resource not found'})
	resp.status_code = 404
	return resp


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/ocr', methods=['POST'])
def ocr():
	file = request.files['file']
	if not file:
		resp = jsonify({'error': 'No File Provided'})
		resp.status_code = 400
		return resp
	try:
		lines = process_image(file).splitlines()
		resp = jsonify({'text': {i: l for i, l in enumerate(lines)}})
		resp.status_code = 200
		return resp
	except:
		resp = jsonify({'error': 'Unprocessable Entity'})
		resp.status_code = 422
		return resp


if __name__ == '__main__':
  app.run(debug=True)
