from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

bp = Blueprint('check', __name__, url_prefix='/check_home')

def allwed_file(filename):
    # .이 있나 없나 체크하는 것과 확장자 확인, 되면 1, 안되면 0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/check')
def check():
    return render_template('check1.html')

@bp.route('/fileUpload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('check1.html')
    elif request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file upload successfully'

@bp.route('/fileUpload/<file>' )
def upload_file(filename):
    return ('check1.html', filename)

@bp.route('/test')
def test():
    return render_template('test.html')
