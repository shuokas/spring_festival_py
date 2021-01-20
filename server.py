# coding:utf-8 
from flask import *
from facedetect import excute
import base64


app = Flask(__name__)

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
    data = request.get_json()
    recognize_info = {'code': 200 ,'info':1,}
    return jsonify(recognize_info), 200

if __name__ == '__main__':
    app.run(port=5000)
