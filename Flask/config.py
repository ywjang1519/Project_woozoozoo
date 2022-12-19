import os
from sqlalchemy import create_engine
import sqlalchemy as db

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI='mysql+pymysql://3pos:threepos@192.168.55.17:3306/3pos'
#SQLALCHEMY_DATABASE_URI='mysql+pymysql://devkiki:910716@210.57.238.194:8572/kiki?useUnicode=true&characterEncoding=utf8&autoReconnect=true&zeroDateTimeBehavior=convertToNull'
# sql 주소 'sqllite:///{}'
SQLALCHEMY_MODIFICATIONS = False
SECRET_KEY="dev" #원래는 길게 작성하지만, test용이니 dev라고 함

# DB 및 테이블 생성 --
engine = db.create_engine('mysql+pymysql://3pos:threepos@192.168.55.17:3306/3pos')
# from sqlalchemy import create_engine
# engine = create_engine('mysql+mysqldb://<username>:<password>@<host>:<port>/<dbname>')
connection = engine.connect()
metadata = db.MetaData()
table = db.Table('user', metadata, autoload=True, autoload_with=engine)
table = db.Table('pet_info', metadata, autoload=True, autoload_with=engine)
table = db.Table('pet_img', metadata, autoload=True, autoload_with=engine)

print(table.columns.keys())