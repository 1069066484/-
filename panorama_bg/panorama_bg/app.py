import os
import argparse

import logging





def parse_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr', type=str,
                        default=r'127.0.0.1:5000')
    parser.add_argument('--__index_html', type=str,
                        default=r'../../PanoramaDisplay_Demo/__index.html')
    parser.add_argument('--basis_bin', type=str,
                        default=r"D:\fduStudy\labZXD\repos\gView\basis\basis_universal\bin\Release\basisu.exe")
    return parser.parse_args()
args = parse_config()


def set_index_html(addr="127.0.0.1:5000", file_index_html="../../PanoramaDisplay_Demo/__index.html"):
    # 10.177.35.99:5000
    assert os.path.exists(file_index_html)
    with open(file_index_html, 'r') as f:
        content = f.read()
    with open(file_index_html.replace("__index", "index"), 'w') as f:
        f.write(content.replace("10.177.35.99:5000", addr))


set_index_html(args.addr, args.__index_html)
from basis import Basis
def make_logger(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logfile = log_file
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.warn('logfile = {}'.format(logfile))
    
    return logger




os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from flask import Flask, render_template, request
from flask_uploads import configure_uploads, UploadSet
from werkzeug.utils import secure_filename
import os, base64
import json
import requests
from flask_cors import *
import shutil
app = Flask(__name__)
CORS(app, supports_credentials=True)

logger = make_logger(__name__ + '.log')
logger.warn("make logger")
basis = Basis(args.basis_bin, out=logger.warn)


# 配置上传文件存放路径
base = os.path.dirname(os.path.abspath(__file__))
base = os.path.join(base, 'static')
app.config['UPLOADS_DEFAULT_DEST'] = base
photo = UploadSet()
configure_uploads(app, photo)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "basis"])
UPLOAD_FOLDER = './static/photo/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upfile', methods=['GET', 'POST'])  # 接受并存储文件
def up_file():
    if request.method == "POST":
        logger.warn(request)
        # 接收图片
        img = 'error'
        file = request.files['panorama']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print(filename, os.path.exists(filename[2:]))
            # print("filename", filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            img = os.path.join(UPLOAD_FOLDER.replace('.',''), filename)

        ims_decompressed = basis.decompress([img[1:] if img[0] == "/" else img])[0]
        logger.warn("{} {}".format(img, ims_decompressed))
        return ims_decompressed

@app.route('/', methods=['get', 'post'])
def index():
    return 'Hello world'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


