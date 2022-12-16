from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from torchvision import transforms
import torch
from PIL import Image
import io

# AI부분 

# 모델 로드
model = torch.load('./pywzz/model/model.pth',map_location='cpu')

# 이미지 정규화/텐서변환 함수
def transform_image(image_bytes):
    transforms_img = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = Image.open(io.BytesIO(image_bytes))
    return transform_image(img).unsqueeze(0)

# 질병예측 함수
def predict_image(image_bytes,model):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # device 객체 생성
    class_model = ['구진/플라크','비듬/각질/상피성잔고리','태선화/과다색소침착','농포/여드름','미란/궤양','결절,종괴']
    tensor_img = transform_image(image_bytes).to(device)
    model.eval() #모델 평가모드로 전환
    with torch.no_grad():
        outputs = model(tensor_img)
        _, preds = torch.max(outputs, 1)
    return class_model[preds] # 예측값 클래스 이름 return


# --------------------------
# 이미지 업로드 부분

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

bp = Blueprint('check', __name__, url_prefix='/check_home')

def allwed_file(filename):
    # .이 있나 없나 체크하는 것과 확장자 확인, 되면 1, 안되면 0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#------------------------------------------------------

#Flask 주소 부분

@bp.route('/check')
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
