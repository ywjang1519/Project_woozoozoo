from pywzz import db

class User(db.Model):
    user_key=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(30),unique=True,nullable=False)
    user_email=db.Column(db.String(120),unique=True,nullable=False)
    user_password=db.Column(db.String(200),nullable=False)
    user_phone=db.Column(db.String(30),nullable=False)

# class PetInfo(db.Model):
#     pet_name = db.Column
#     pet_birth = db.Column
#     pet_sex = db.Column
#     pet_bred = db.Column
#     profile_img = db.Column(db.String(100), default='default.png')
