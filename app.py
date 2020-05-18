import os
import urllib.request
import uuid
import zipfile
from flask import Flask, request
from pdf2image import convert_from_path

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def index():
    tmp_dir  = './tmp'

    if 'pdf' in request.args:
        rhash    = uuid.uuid4().hex
        work_dir = os.path.join(tmp_dir, rhash)
        filename = request.args['pdf']

        os.mkdir(work_dir)

        # Get file
        uo = urllib.request.URLopener()
        uo.retrieve(filename, os.path.join(work_dir, 'tmp.pdf'))

        # Create images
        images_from_path = convert_from_path(os.path.join(work_dir, 'tmp.pdf'), output_folder = work_dir)

        image_dir = os.path.join(work_dir, 'output')
        os.mkdir(image_dir)

        i = 1
        for page in images_from_path:
            page.save(os.path.join(image_dir, 'page-' + str(i) + '.webp'), format = 'WEBP', lossless = True)
            i = i + 1

        # Create zip
        zipf = zipfile.ZipFile(os.path.join(tmp_dir, rhash + '.zip'), 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(image_dir):
            for f in files:
                zipf.write(os.path.join(root, f), f)
        zipf.close()

        # Clean up
        for root, dirs, files in os.walk(work_dir):
            for f in files:
                os.remove(os.path.join(root, f))
        os.rmdir(image_dir)
        os.rmdir(work_dir)

        return request.base_url + 'tmp/' + rhash + '.zip'
    else:
        return ''

if __name__ == '__main__':
    app.run(threaded = False, port = 5000)
