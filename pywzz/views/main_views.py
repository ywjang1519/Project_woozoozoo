from flask import Blueprint,render_template

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

# @bp.route('/signup')
# def signup():
#     print('signup')
#     return render_template('auth/signup.html')
#
# @bp.route('/login')
# def login():
#     return render_template('auth/login.html',)