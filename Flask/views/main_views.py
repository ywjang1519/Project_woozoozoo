from flask import Blueprint,render_template

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/signup')
def signup():
    print('signup')
    print()
    return render_template('index.html')

# @bp.route('/movie')
# def movie():
#     return render_template('movie.html')

