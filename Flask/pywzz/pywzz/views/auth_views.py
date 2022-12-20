from flask import Blueprint,render_template,request,url_for,flash,session, g
from pywzz.forms import UserCreateForm,UserLoginForm
from pywzz import db
from pywzz.models import User
from datetime import datetime
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('signup',methods=('GET','POST'))
def signup():
    form=UserCreateForm()
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
    return render_template('auth/signup_bts.html',form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(user_name=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.user_password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."

        if error is None:
            session.clear()
            session['user_name'] = user.user_name
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login_bts.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_name = session.get('user_name')
    if user_name is None:
        g.user = None
    else:
        g.user = user_name

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.home'))