from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

bp = Blueprint('main', __name__, url_prefix='/')

def allwed_file(filename):
    # .이 있나 없나 체크하는 것과 확장자 확인, 되면 1, 안되면 0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/fileUpload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file upload successfully'

@bp.route('/fileUpload/<file>' )
def upload_file(filename):
    return ('home.html', filename)

@bp.route('/signup')
def signup():
    return render_template('signup.html')

@bp.route('/login')
def login():
    return render_template('login.html')