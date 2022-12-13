from pywzz import db

class User(db.Model):
    user_key=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(30),unique=True,nullable=False)
    user_email=db.Column(db.String(120),unique=True,nullable=False)
    user_password=db.Column(db.String(30),nullable=False)
    user_age=db.Column(db.Integer,nullable=False)
