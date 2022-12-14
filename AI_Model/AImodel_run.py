import torch
import torch.nn as nn
import torch.optim as optim

import torchvision
from torchvision import datasets, models, transforms

import numpy as np
import time
import os
from glob import glob
from PIL import Image


def airun(img,model):
    '''
    img : image data -> PIL.Image.open() 등으로 데이터 열어야됩니다!
    model : 딥러닝 학습 모델 넣어주세요. torch에서 로드한 모델로 넣어주세요!
    결과 : 클래스 이름 -> string으로 돌려줍니다. 사용하려면 print() 함수 등을 써주세요.
    '''
    class_model = ['구진/플라크','비듬/각질/상피성잔고리','태선화/과다색소침착','농포/여드름','미란/궤양','결절,종괴']
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # device 객체 생성

    #데이터 전처리
    transforms_test = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = transforms_test(img).unsqueeze(0).to(device)
    model.eval()

    with torch.no_grad():
        outputs = model(img)
        _, preds = torch.max(outputs, 1)
    return class_model[preds]


# 시험가동입니다~
# if __name__ == '__main__':

#     model = torch.load("C:/Users/user/Documents/project_final/AI_Model/model.pth",map_location='cpu')
#     img = Image.open("C:/Users/user/Documents/project_final/AI_Model/IMG_D_A6_495860.jpg")
#     print(airun(img,model))

