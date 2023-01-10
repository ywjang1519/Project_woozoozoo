# 라이브러리 import단
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from werkzeug.utils import secure_filename
from pywzz.models import PetImg, Disease, User
from pywzz import db, forms
import os
from torchvision import transforms
import torch
from PIL import Image
import cv2
from .auth_views import load_logged_in_user
#---------------------------------------
# AI모델 구동 위한 부분
model = torch.load('pywzz/model/model.pth',map_location='cpu')
#map_location -> cpu/gpu 어떤걸 쓸껀지 물어보는 것 -> 학습은 GPU로 해서 CPU만 있으면 map_location='cpu' 써야 함

model.eval()
def transform_image(img_file):
    transform_image = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = Image.open(img_file).convert('RGB')
    return transform_image(img).unsqueeze(0)

def model_run(img_file):
    #class_model = ['구진/플라크','비듬/각질/상피성잔고리','태선화/과다색소침착','농포/여드름','미란/궤양','결절,종괴']
    img_tensor = transform_image(img_file)
    with torch.no_grad():
        outputs = model(img_tensor)
        _, preds = torch.max(outputs, 1)

        # DB테이블에서 증상 가져오기
        disease_category = Disease.query.filter_by(disease_id=int(preds)+1).\
            with_entities(Disease.disease_category,Disease.disease_name,Disease.disease_content,Disease.disease_cause,Disease.disease_solution).first()

    return disease_category

#-------------------------------------
# 이미지 파일 처리 위한 부분
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allwed_file(filename):
    # .이 있나 없나 체크하는 것과 확장자 확인, 되면 1, 안되면 0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#----------------------------------------------------

# Flask 웹 구동부
bp = Blueprint('check', __name__, url_prefix='/check')

@bp.route('/')
def check():
    # @load_logged_in_user()
    if g.user == None:
        return redirect(url_for('auth.login'))
    else:
        return render_template('check/check.html')

@bp.route('/upload', methods = ['GET', 'POST'])
def upload():
    # @load_logged_in_user()
    if request.method == 'GET':
        return redirect(url_for('check.check'))

    elif request.method == 'POST':
        f = request.files['data']
        # current_path=os.getcwd()

        dir_path='pywzz/static/pet_img/'
        if os.path.isdir(dir_path):
            os.makedirs('pywzz/static/pet_img/',exist_ok=True)

        path=dir_path+str(g.user) #경로
        send_name= 'pet_img/'+g.user+'/' + secure_filename(f.filename)
        f_name=path + '/' + secure_filename(f.filename)

        os.makedirs(path,exist_ok=True)
        f.save(f_name)

        # mysql
        petimage=PetImg(img=path+'/'+secure_filename(f.filename))
        db.session.add(petimage)
        db.session.commit()

        return render_template('check/check_result.html',pet_name="시월이",send_name=send_name, model_run=model_run(f_name))
        # return redirect(url_for('check.result'))
        # return model_run(petimage.img)

@bp.route('/upload/<filename>')
def upload_file():
    form = forms.PetImgForm
    filename=PetImg.query.filter_by(img=form.img.data)
    db.session.add(filename)
    db.session.commit()

    _next = request.args.get('next', '')
    return redirect(url_for('check/check.html'))

@bp.route('/result',methods = ['GET', 'POST'])
def result():
    if request.method == 'GET':
        # img_file=PetImg.query.filter_by(id=)
        # print(img_file)
        # model_run(img_file)
        return render_template('check/check_result.html')

    elif request.method == 'POST':
        form = forms.UserLoginForm
        user = User.query.filter_by(user_name=form.username.data).first()
        return redirect(url_for('check.model_run'))

@bp.before_app_request
def authenticate():
    # request.authorization username이 있는 경우 g.user에 할당
    g.user = 'Anonymous' if not request.authorization else request.authorization['username']
    g.petimg = 'Anonymous' if not request.authorization else request.authorization['pet_image']
    g.model_run = 'Anonymous' if not request.authorization else request.authorization['model_run']

@bp.before_app_request
def load_logged_in_user() :
    user_name = session.get('user_name')
    if user_name is None:
        g.user = None
    else:
        g.user = user_name
        # g.user = User.query.get(user_id) 인데

# @bp.before_app_request
# def clear_page():
#     session.clear()
#     return render_template('check/check_result.html')