import os
import subprocess
import sys
import logging
import shutil
import tempfile
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff'])


@app.errorhandler(404)
def not_found(error):
  resp = jsonify({
      'status': 404,
      'message': 'Resource not found'
  })
  resp.status_code = 404
  return resp


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
	file = request.files['file']
	if not file or not allowed_file(file.filename):
		resp = jsonify({'status': 415,'message': 'Unsupported Media Type'})
		resp.status_code = 415
		return resp

	folder = tempfile.mkdtemp()
	input_file = os.path.join(folder, secure_filename(file.filename))
	file.save(input_file)
	output_file = os.path.join(folder, 'output')

	command = ['tesseract', input_file, output_file, '-l', 'spa+eng']
	proc = subprocess.Popen(command, stderr=subprocess.PIPE)
	proc.wait()

	output_file += '.txt'

	if os.path.isfile(output_file):
		f = open(output_file)
		resp = jsonify({'status': 200,'ocr': {k: v for k, v in enumerate(f.read().splitlines())}})
	else:
		resp = jsonify({'status': 422,'message': 'Unprocessable Entity'})
		resp.status_code = 422
	shutil.rmtree(folder)
	return resp


if __name__ == '__main__':
  app.run(debug=True)
