#폼을 어떤걸로 쓸지 정의를 하는 곳 
#메일 형식인지, 문자인지, 암호화할지 등

from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    username=StringField('사용자 이름',validators=[DataRequired(),Length(min=3,max=20)])
    password1=PasswordField('비밀번호',validators=[DataRequired(),EqualTo('password2','비밀번호가 다릅니다.'),Length(min=4,max=20)])
    password2=PasswordField('비밀번호 확인',validators=[DataRequired()])
    email=EmailField('이메일',validators=[DataRequired(),Email()])
    phone=StringField('전화번호',validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])