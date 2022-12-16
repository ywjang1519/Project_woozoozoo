from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for,\
    flash, send_file, send_from_directory
from flask_uploads import IMAGES
from werkzeug.utils import secure_filename

bp = Blueprint('main', __name__, url_prefix='/')

# #업로드 될 확장자 제한
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#
# #업로드 될 경로
# UPLOAD_FOLDER = '/.uploads'
#
# def allwed_file(filename):
#     # .이 있나 없나 체크하는 것과 확장자 확인, 되면 1, 안되면 0
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def home():
    return render_template('check1.html')

@bp.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('check1.html')
    elif request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file upload successfully'

@bp.route('/test')
def test():
    return render_template('test1.html')