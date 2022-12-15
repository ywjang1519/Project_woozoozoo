# 라이브러리 import단
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import io
from torchvision import transforms
import torch
from PIL import Image
#---------------------------------------
# AI모델 구동 위한 부분
model = torch.load('pywzz/model/model.pth',map_location='cpu')
model.eval()
def transform_image(image_byte):
    transform_image = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = Image.open(io.BytesIO(image_byte))
    return transform_image(img).unsqueeze(0)

def model_run(image_byte):
    class_model = ['구진/플라크','비듬/각질/상피성잔고리','태선화/과다색소침착','농포/여드름','미란/궤양','결절,종괴']
    img_tensor = transform_image(image_byte)
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
    return render_template('check1.html')

@bp.route('/fileUpload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('check1.html')
    elif request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file upload successfully'

@bp.route('/fileUpload/<file>' )
def upload_file(filename):
    return ('check1.html', filename)

@bp.route('/test')
def test():
    return render_template('test.html')
