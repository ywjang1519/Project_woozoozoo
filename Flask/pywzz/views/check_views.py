# 라이브러리 import단
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from werkzeug.utils import secure_filename
from pywzz.models import PetImg
from pywzz import db
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
    class_model = ['구진/플라크','비듬/각질/상피성잔고리','태선화/과다색소침착','농포/여드름','미란/궤양','결절,종괴']
    img_tensor = transform_image(img_file)
    with torch.no_grad():
        outputs = model(img_tensor)
        _, preds = torch.max(outputs, 1)
    return class_model[preds]

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
        current_path=os.getcwd()
        path=current_path+'/pywzz/tmp_img/'+str(g.user)

        os.makedirs(path,exist_ok=True)
        f.save(path+'/'+secure_filename(f.filename))

        petimage=PetImg(img=path+'/'+secure_filename(f.filename))
        db.session.add(petimage)
        db.session.commit()

        return render_template('check/check_result.html', )
        # return redirect(url_for('check.result'))

@bp.route('/upload/<filename>')
def upload_file():
    filename=PetImg.query.filter_by(img=form.img.data)
    db.session.add(filename)
    db.session.commit()
    return redirect(url_for('check/check.html'))

@bp.route('/result',methods = ['GET', 'POST'])
def result():
    if request.method == 'GET':
        # img_file=PetImg.query.filter_by(id=)
        # print(img_file)
        # model_run(img_file)
        return render_template('check/check_result.html')
    elif request.method == 'POST':
        return redirect(url_for('model_run'))

@bp.before_app_request
def load_logged_in_image():
    pet_image = session.get('image')
    if pet_image is None:
        g.pet_image = None
    else:
        g.pet_image = pet_image

# @bp.before_app_request
# def clear_page():
#     session.clear()
#     return render_template('check/check_result.html')