from pywzz import db

class User(db.Model):
    __table_name__ = 'user'

    user_key=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(30),unique=True,nullable=False)
    user_email=db.Column(db.String(120),unique=True,nullable=False)
    user_password=db.Column(db.String(200),nullable=False)
    user_phone=db.Column(db.String(30),nullable=False)

class PetInfo(db.Model):
    __table_name__ = 'pet_info'

    petInfo_key=db.Column(db.Integer,primary_key=True)
    pet_name = db.Column(db.String(30),nullable=False)
    pet_birth = db.Column(db.String(120),nullable=False)
    pet_sex = db.Column(db.String(10),nullable=False)
    pet_bred = db.Column(db.String(10),nullable=False)
    profile_img = db.Column(db.String(100), default='default.png')

class PetImg(db.Model):
    __table_name__ = 'pet_img'

    id=db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(100), default='dog.png')

# Question & Answer
class Question(db.Model):
    __table_name__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_key', ondelete='CASCADE'), nullable=True, server_default='1')
    user = db.relationship('User', backref=db.backref('question_set'))

class Answer(db.Model):
    __table_name__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_key', ondelete='CASCADE'), nullable=True, server_default='1')
    user = db.relationship('User', backref=db.backref('answer_set'))

class Disease(db.Model):
    __table_name__ = 'disease'

    disease_id=db.Column(db.Integer, primary_key=True)
    disease_category=db.Column(db.String(200), nullable=True)
    disease_name=db.Column(db.String(200), nullable=True)
    disease_content=db.Column(db.String(100), nullable=True)
    disease_cause=db.Column(db.String(200), nullable=True)
    disease_solution=db.Column(db.String(500), nullable=True)

class RealTime(db.Model):
    __table_name__='realtime'

    product_id = db.Column(db.Integer, primary_key=True)
    product_category = db.Column(db.String(100), nullable=True)
    product_name=db.Column(db.String(100), nullable=True)
    product_url=db.Column(db.String(1500), nullable=True)