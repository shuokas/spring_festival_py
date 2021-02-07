# coding:utf-8
import cv2
from PIL import Image
from io import BytesIO
from faceswap import swap
import base64
import numpy
import os
import random
import re


def detect(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 将图片转化成灰度

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")  # 加载级联分类器模型
    face_cascade.load('static/haarcascade_frontalface_alt2.xml')  # 一定要告诉编译器文件所在的具体位置
    '''此文件是opencv的haar人脸特征分类器'''
    locs = face_cascade.detectMultiScale(gray, 1.3, 5)

    faces = []

    for (x, y, w, h) in locs:
        a, b, c, d = x, y, x + w, y + h
        face = img[b:d, a:c]
        faces.append(face)
    return faces

def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    # print(byte_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return img

def save_temp_imgs(list):
    temp_imgs = []
    for l in list:
        pic = Image.open(l)
        img = cv2.cvtColor(numpy.asarray(pic), cv2.COLOR_RGB2BGR)
        temp_imgs.append(img)
    return temp_imgs


def join(seamless_ims):
    ims = []
    print('seamless_ims**********',seamless_ims)
    for seamless_im in seamless_ims:
        image = Image.fromarray(cv2.cvtColor(seamless_im, cv2.COLOR_BGR2RGB))
        ims.append(image)

    width = 0
    for im in ims:
        w, height = im.size
        width += w
        
    print(ims)
    # 创建空白长图
    result = Image.new(ims[0].mode, (width, height))


    # 拼接图片
    temp = 0
    for im in ims:
        w, height = im.size
        result.paste(im, box=(temp, 0))
        temp += w

    # img = cv2.cvtColor(numpy.asarray(result), cv2.COLOR_RGB2BGR)

    img = cv2.cvtColor(numpy.asarray(result), cv2.COLOR_RGB2RGBA)


    return img


def get_moulds_path():
    # path = 'static/moulds/%s/%s/%s' % (sex, major, dgree)
    path = 'static/moulds/'
    # 可以根据参数匹配不同的图片
    # 根据用户选择的不同配置展示不同的人物基座

    # 人的模板
    return path


def process(faces, target_template):
    seamless_ims = []

    # moulds = os.listdir(moulds_path)
    # print('moulds_path**********',moulds_path)
    n = len(faces)
    for i in range(n):
        face = faces[i]
        # x = random.randint(0, len(moulds)-1)
        # mould = moulds_path + '/' + moulds[x]
        # mould = target_template + '/8.png'
        print('face**********',face)
        print('target_template**********',target_template)
        # 将mould 改为文件
        # pic = base64_to_image(target_template)
        # img = cv2.cvtColor(numpy.asarray(pic), cv2.COLOR_RGB2BGR)
        # temp_imgs.append(img)
        
        # 模板图（原图->模板）
        seamless_im = swap(face, target_template)
        
        seamless_ims.append(seamless_im)
        
    return seamless_ims


def load_background(img):
    # img_back_path = 'static/background/'

    # list = os.listdir(img_back_path)

    # x = random.randint(0, len(list) - 1)
    # 固定背景图 
    img_back = cv2.imread('static/background/1111.jpg')

    # 日常缩放
    height, width, channels = img.shape
    img_back = cv2.resize(img_back, (width + 400, height), interpolation=cv2.INTER_CUBIC)

    # 转换hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 获取mask
    lower_blue = numpy.array([100, 75, 75])
    upper_blue = numpy.array([101, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 腐蚀膨胀
    erode = cv2.erode(mask, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)

    # 遍历替换
    center = [0, 200]  # 在新背景图片中的位置
    for i in range(height):
        for j in range(width):
            if dilate[i, j] == 0:
                try:
                    img_back[center[0] + i, center[1] + j] = img[i , j]  # 此处替换颜色，为BGR通道
                except:
                    pass

    img_back = img_back[:, :, ::-1]
    img_with_background = Image.fromarray(img_back)

    return img_with_background


def excute(sourceFile, targetFile):
    # print(list)
    paths = save_temp_imgs(sourceFile)
    print('paths**********',paths)
    faces_ = []
    for path in paths:
        print('path***********',path)
        faces = detect(path)
        faces_ += faces

    # 人物固定了（如果做更换脸型、发型可根据此改造）
    # 路径
    print(faces)
    # 转换为文件
    print('*********************tttatgasda',base64_to_image(targetFile))
    moulds_path = get_moulds_path()
    print('type@@@@@@@@@@@@@@@@@@',type(targetFile))
    
    img_data = base64.b64decode(targetFile)
    # print('img_data*********',img_data)
    nparr = numpy.fromstring(img_data, numpy.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print('nparr@#@#@#@#@#@#',img_np)
    # 读取图片（可以做成直接读取服务器）
    print('faces_*********',faces_)
    
    # seamless_ims = process(faces_, moulds_path)
    seamless_ims = process(faces_, img_np)
    print('seamless_ims!!!!!!!!!!!!!!!!!!!!!!!!!!!',seamless_ims)
    print('np.uint8(img)*******',numpy.uint8(seamless_ims))
    # seamless_ims = process(faces_, base64_to_image(targetFile))

    img = join(seamless_ims)
    # print(img)
    # img_with_background = load_background(img)
    # 读取背景转换为fromarray
    img_with_background = Image.fromarray(img)

    # print(img_with_background)

    f = BytesIO()

    img_with_background.save(f, "png")

    return f
