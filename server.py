# coding:utf-8 
from flask import *
from facedetect import excute
import base64
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

#设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ys258311!@#@39.106.93.128:3306/spring_festival'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ys258311!@#@localhost/spring_festival'
 
#设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# 类

class ClothesComponents(db.Model):
    # 定义表名
    __tablename__ = 'ClothesComponents'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    thumbnailUrl = db.Column(db.String(255))
    imgType = db.Column(db.String(255)) 
    
@app.route('/swap', methods=['post'])
def swap_page():
    
    ims = request.files.getlist('file')
    sex = request.form.get('sex')
    major = request.form.get('major')
    degree = request.form.get('degree')

    f = excute(ims, sex, major, degree)
    img_stream = base64.b64encode(f.getvalue()).decode()
    recognize_info = {'code': 200 ,'message': '请求成功','data': {'img': img_stream}}
    return jsonify(recognize_info), 200
    # return render_template('result.html', img_stream=img_stream)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def post_Data():
    images = ClothesComponents.query.all()
    print(ClothesComponents.query.all())
    data = []
    for i in images:
        print(i.id)
        print(i.thumbnailUrl)
        print(i.imgType)
        data.append({'id': i.id,'url':i.thumbnailUrl,'type':i.imgType})
        
    # data = request.get_json()
    recognize_info = {'code': 200 ,'data':data,}
    return jsonify(recognize_info), 200

if __name__ == '__main__':
    app.run(port=5000)
