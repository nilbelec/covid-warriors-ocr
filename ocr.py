import os
import subprocess
import tempfile
from werkzeug.utils import secure_filename


def process_image(file):
	folder = tempfile.mkdtemp()
	input_file = os.path.join(folder, secure_filename(file.filename))
	file.save(input_file)

	output_file = os.path.join(folder, 'output')
	command = ['tesseract', input_file, output_file, '-l', 'spa+eng']
	subprocess.run(command)

	with open(output_file + '.txt', encoding="UTF-8") as f:
		return f.read()
