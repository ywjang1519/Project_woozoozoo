from werkzeug.utils import redirect
from flask import Blueprint,render_template,request,url_for,flash,session, g

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('main.home'))

@bp.route('/home')
def home():
    return render_template('main/home.html')

@bp.route('/profile')
def profile():
    return render_template('index.html')

@bp.route('/test')
def test():
    return render_template('check/check.html')
