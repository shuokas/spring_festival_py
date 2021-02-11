# coding:utf-8
from flask import *
from facedetect import excute
import base64
import pymysql
from flask_sqlalchemy import SQLAlchemy
import time

pymysql.install_as_MySQLdb()

app = Flask(__name__)


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = 'Ys258311!@#'
    database = 'spring_festival'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@39.106.93.128:3306/%s' % (
        user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    app.debug = True


# 读取配置
app.config.from_object(Config)
# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)

# 衣服模板类


class ClothesComponents(db.Model):
    # 定义表名
    __tablename__ = 'ClothesComponents'
    # 定义字段
    part_id = db.Column(db.Integer, primary_key=True)
    thumbnailUrl = db.Column(db.String(255))
    imgType = db.Column(db.String(255))
    artworkUrl = db.Column(db.String(255))
    sex = db.Column(db.Integer)

# 家庭表


class Family(db.Model):
    # 定义表名
    __tablename__ = 'Family'
    # 定义字段
    family_id = db.Column(db.Integer, primary_key=True)
    family_count = db.Column(db.String(255))
    baseInfo = db.Column(db.String(255))

# 用户生成结果表


class UserPortrait(db.Model):
    # 定义表名
    __tablename__ = 'UserPortrait'
    # 定义字段
    user_id = db.Column(db.Integer, primary_key=True)
    target_body = db.Column(db.String(255))
    head_url = db.Column(db.String(255))
    top_url = db.Column(db.String(255))
    bottom_url = db.Column(db.String(255))
    sex = db.Column(db.Integer)
    source_template = db.Column(db.String(255))

# 用户表


class FamilyUser(db.Model):
    # 定义表名
    __tablename__ = 'FamilyUser'
    # 定义字段
    user_id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer)
    uuid = db.Column(db.Integer)

# 第一步选择拍照类型时收集 人数 + 类型 + 微信号


@app.route('/carryBaseInfo', methods=['POST'])
def carryBaseInfo():
    # 判断如果有id则更新选择的信息，没有id则新增
    # if condition:
    #       pass
    family_count = request.json.get('family_count')
    baseInfo = request.json.get('baseInfo')
    # 插入一条角色数据
    # family_info = Family(family_count=family_count,baseInfo=baseInfo)
    # db.session.add(family_info)
    # db.session.commit()
    # join_img(

    print(family_count)
    print(baseInfo)

    response_info = {
        'code': 200,
        'message': '请求成功',
        'data': {}
    }
    return jsonify(response_info), 200
# 选择零件-获取具体图片


@app.route('/getImgPartList', methods=['POST'])
def get_img_part_list():
    img_type = request.json.get('imgType')
    img_sex = request.json.get('sex')
    res_part = ClothesComponents.query.filter_by(
        imgType=img_type, sex=img_sex).all()
    count = 0
    first_row = []
    second_row = []
    for i in res_part:
        print(i)
        count += 1
        if count % 2 > 0:
            second_row.append({'part_id': i.part_id,
                               'thumbnailUrl': i.thumbnailUrl,
                               'type': i.imgType,
                               'artworkUrl': i.artworkUrl,
                               'sex': i.sex
                               })
        else:
            first_row.append({'part_id': i.part_id,
                              'thumbnailUrl': i.thumbnailUrl,
                              'type': i.imgType,
                              'artworkUrl': i.artworkUrl,
                              'sex': i.sex
                              })

    response_info = {
        'code': 200,
        'message': '请求成功',
        'data': {'first_row': first_row,
                 'second_row': second_row
                 }
    }
    return jsonify(response_info), 200


# 第二步选择人物模板

@app.route('/saveImageTemplate', methods=['POST'])
def save_image_template():
    # family_id,family_user_id,Weid,head,top,bottom
    # 存入图片id，进行编辑回显数据  UserPortrait
    head = request.json.get('head')
    top = request.json.get('top')
    bottom = request.json.get('bottom')
    source_template = request.json.get('source_template')
    sex = request.json.get('sex')
    uuid = request.json.get('uuid')

    # template_info = UserPortrait(
    #     head_url=head, top_url=top, bottom_url=bottom, source_template=source_template,sex=sex)
    # res = UserPortrait.query.all()

    user_info = FamilyUser.query.filter_by(uuid=uuid).first()
    user_id = user_info.user_id
    # print(UserPortrait.query.filter_by(user_id=user_id).first())
    # 固定查询
    UserPortrait.query.filter_by(user_id=8).update({
        'head_url': head,
        'top_url': top,
        'bottom_url': bottom,
        'source_template': source_template,
        'sex': sex
    })

    # for i in res:
    #     print(i.sex)
    #     print(i.target_body)
    # user_id = db.Column(db.Integer, primary_key=True)
    # target_body = db.Column(db.String(255))
    # db.session.add(template_info)
    # db.session.commit()
    response_info = {
        'code': 200,
        'message': '请求成功',
        'data': {'head': head, 'top': top, 'bottom': bottom, 'source_template': source_template, }
        # 'transform_img': swap_img
    }
    return jsonify(response_info), 200

# 读取人物模板


@app.route('/bodyTemplate', methods=['POST'])
def load_template():
    uuid = request.json.get('uuid')
    user_info = FamilyUser.query.filter_by(uuid=uuid).first()
    user_id = user_info.user_id

    res_part = UserPortrait.query.filter_by(user_id=user_id).all()
    result = ''
    for i in res_part:
        result = str(i.source_template)

    response_info = {
        'code': 200,
        'message': '请求成功',
        'data': result
    }
    return jsonify(response_info), 200


@app.route('/swapFace', methods=['POST'])
def swap_face():

    sourceFile = request.files.getlist('sourceFile')
    targetFile = request.form.get('targetFile')
    print('sourceFile******************', sourceFile)
    f = excute(sourceFile, targetFile)
    img_stream = base64.b64encode(f.getvalue()).decode()

    result_info = {'code': 200, 'message': '请求成功',
                   'data': img_stream}
    return jsonify(result_info), 200

# 保存用户id


@app.route('/saveUserInfo', methods=['POST'])
def save_user_info():
    # uuid = request.json.get('uuid')
    # family_count = request.json.get('family_count')
    # # 查询数据库，如果存在 则加入，不存在则创建
    # # 先查询家庭id是否存在。如果不存在，先操作家庭数据
    # # 精确查找用的first

    # user_result = FamilyUser.query.filter_by(uuid=uuid).first()
    # print('222222222222',user_result)
    # # 存在uuid
    # if user_result:
    #     family_id = user_result.family_id
    #     if family_id:
    #         print('有，直接uodata')
    #         print(family_id)
    #     else:
    #         # 有uuid 没有family的情况则创建一条family数据
    #         family_info = Family(family_count=family_count)
    #         db.session.add(family_info)
    #         db.session.commit()
    # else:
    #     print('否则')
        # 未找到数据时的情况(没有的话则创建)
        # user_info = FamilyUser(uuid=uuid)
        # family_info = Family(family_count=family_count)
        
        # db.session.add(user_info)
        # db.session.add(family_info)
        # # 创建uuid的时候同步创建familyid
        
        # db.session.commit()
        


    data = []
    result_info = {'code': 200, 'message': '请求成功',
                   'data': data}
    return jsonify(result_info), 200


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def post_Data():
    # images = ClothesComponents.query.all()
    # print(ClothesComponents.query.all())
    # data = []
    # for i in images:
    #     print(i.part_id)
    #     print(i.thumbnailUrl)
    #     print(i.imgType)
    #     data.append(
    #         {'id': i.part_id, 'url': i.thumbnailUrl, 'type': i.imgType})
    test = request.json.get('test')
    print(test)
    # data = request.get_json()
    data = {
        'test': test
    }
    recognize_info = {'code': 200, 'data': data, }
    return jsonify(recognize_info), 200


if __name__ == '__main__':
    app.run(port=5000)
