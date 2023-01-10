from werkzeug.utils import redirect
from flask import Blueprint,render_template,request,url_for,flash,session, g
from pywzz.forms import PetInfoForm

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('main.home'))

@bp.route('/home')
def home():
    return render_template('main/home.html')

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/profile')
def profile():
    form=PetInfoForm()
    if request.method=='POST' and form.validate_on_submit():
        user=User.query.filter_by(user_name=form.username.data).first()
        if not user:
            user=User(user_name=form.username.data, user_password=generate_password_hash(form.password1.data),
                      user_email=form.email.data, user_phone=form.phone.data )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 유저입니다.')
    return render_template('main/profile.html')

@bp.route('/test')
def test():
    return render_template('question/realtime.html')

