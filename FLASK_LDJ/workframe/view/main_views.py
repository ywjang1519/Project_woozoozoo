from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.utils import secure_filename


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/fileUpload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file upload successfully'

@bp.route('/signup')
def signup():
    return render_template('signup.html')

@bp.route('/login')
def login():
    return render_template('login.html')