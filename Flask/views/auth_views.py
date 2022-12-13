from flask import Blueprint,render_template,request,url_for,flash,session
from pywzz.forms import UserCreateForm
from pywzz import db
from pywzz.models import User
from datetime import datetime
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('signup',methods=('GET','POST'))
def signup():
    form=UserCreateForm()

    print('----1. 유저 아이디')
    if request.method=='POST' and form.validate_on_submit():
        print('----2. 이미 존재하는 지?')
        user=User.query.filter_by(user_name=form.username.data).first()

        print('----3.')
        if not user:
            user=User(user_name=form.username.data, user_password=generate_password_hash(form.password1.data),
                      user_email=form.email.data, user_phone=form.phone.data )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 유저입니다.')
    return render_template('auth/signup.html',form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(user_name=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

