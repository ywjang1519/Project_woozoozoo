from flask import Blueprint, render_template, request, redirect, url_for, session, g, jsonify, make_response
from pywzz.models import PetDictionary
from pywzz.forms import PetDictionaryForm
from pywzz import db

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import random
import numpy as np
import csv
import pandas as pd

#-------------------------------------
# 지수로그 없애기 위해 소수점 6자리까지만
np.set_printoptions(precision=6, suppress=True)
# 한국어 모델 불러오기
model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
'''
#임베딩 잘되는지 테스트
sentence = ['안녕하세요 테스트입니다.','반갑습니다. 테스트입니다.']
embeding = model.encode(sentence)
embeding.shape
df = pd.read_csv('ChatbotData.csv')
# 매번 채팅 들어올때 임베딩하면 시간이 너무 오래 걸려 챗봇 질문 데이터 임베딩해서 csv로 저장하기

with open('embeding.csv', 'w') as file:
    mapdata = []
    write = csv.writer(file)
    for temp in df['Q']:
        t = model.encode(temp)
        mapdata.append(t)

    write.writerows(mapdata)
'''
# csv 불러오기
df1 = pd.read_csv('C:/PythonPRJ/woozoozoo/pywzz/static/file/embeding.csv', header=None)
df1.info()
# 챗봇 데이터 불러오기
df = pd.read_csv('C:/PythonPRJ/woozoozoo/pywzz/static/file/ChatbotData.csv')
df.iloc[0]

# 챗봇 함수 입력받은 텍스트와 embeding 유사도 체크후 원본 챗봇에 cos컬럼 만든후 상위 정렬
def chatbot_text(text):
    em_result = model.encode(text)
    co_result = []
    for temp in range(len(df1)):
        data = df1.iloc[temp]
        co_result.append(cosine_similarity([em_result], [data])[0][0])
    df['cos'] = co_result
    df_result = df.sort_values('cos', ascending=False)
    r = random.randint(0, 5)
    return df_result.iloc[r]


# app 구동부 -----------------------------
# chatbot_text('테스트')

# Flask 웹 구동부
bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@bp.route('/', methods=['GET', 'POST'])
def dictionary():
    form = PetDictionaryForm()
    if request.method == 'GET':
        num = 37797004
        pet_url = 'https://terms.naver.com/entry.naver?docId=' + str(num) + '&categoryId=58401&cid=42883'
        print(pet_url)
        return render_template('chatbot/pet_dictionary.html')

    elif request.method == 'POST':
        num = 37797004
        # pet_url= PetDictionary.query.filter_by(pet_index=3397003+num).with_entities(PetDictionary.pet_url).first()
        # pet_url=PetDictionary.query.filter_by(dictionary_category=form.category.data).with_entities(PetDictionary.pet_url)
        pet_url = 'https://terms.naver.com/entry.naver?docId=' + str(num) + '&categoryId=58401&cid=42883'
        print(pet_url)
        return render_template('chatbot/pet_dictionary.html')

@bp.route('/dictionary_result',methods = ['GET', 'POST'])
def dictionary_result():
    if request.method == 'GET':
        # return render_template('chatbot/pet_dictionary.html')
        return redirect(url_for('chatbot_text'))

    elif request.method == 'POST':
        # form = forms.UserLoginForm
        # user = User.query.filter_by(user_name=form.username.data).first()
        return redirect(url_for('chatbot_text'))

@bp.route('/test',methods = ['GET', 'POST'])
def test():
    if request.method == 'GET':
        value = request.args.get('value', default = '배고파', type = str)
        result = chatbot_text(value)
        print(result[0])
        return result[1]

# @bp.route('/test_2',methods = ['GET', 'POST'])
# def test_2():
