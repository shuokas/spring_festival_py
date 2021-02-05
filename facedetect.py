# coding:utf-8
import cv2
from PIL import Image
from io import BytesIO
from faceswap import swap
import numpy
import os
import random


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


def save_temp_imgs(list):
    temp_imgs = []
    for l in list:
        pic = Image.open(l)
        img = cv2.cvtColor(numpy.asarray(pic), cv2.COLOR_RGB2BGR)
        temp_imgs.append(img)

    return temp_imgs


def join(seamless_ims):
    ims = []

    for seamless_im in seamless_ims:
        image = Image.fromarray(cv2.cvtColor(seamless_im, cv2.COLOR_BGR2RGB))
        ims.append(image)

    width = 0
    for im in ims:
        w, height = im.size
        width += w

    # 创建空白长图
    result = Image.new(ims[0].mode, (width, height))


    # 拼接图片
    temp = 0
    for im in ims:
        w, height = im.size
        result.paste(im, box=(temp, 0))
        temp += w

    # img = cv2.cvtColor(numpy.asarray(result), cv2.COLOR_RGB2BGR)

    img = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2RGBA)


    return img


def get_moulds_path(sex, major, dgree):
    # path = 'static/moulds/%s/%s/%s' % (sex, major, dgree)
    path = 'static/moulds/'
    # 可以根据参数匹配不同的图片
    # 根据用户选择的不同配置展示不同的人物基座

    # 人的模板
    return path


def process(faces, moulds_path):
    seamless_ims = []

    # moulds = os.listdir(moulds_path)

    n = len(faces)
    for i in range(n):
        face = faces[i]
        # x = random.randint(0, len(moulds)-1)
        # mould = moulds_path + '/' + moulds[x]
        mould = moulds_path + '/8.png'
        seamless_im = swap(face, mould)
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


def excute(list, sex, major, degree):
    print(list)
    paths = save_temp_imgs(list)


    print(paths)
    faces_ = []

    for path in paths:
        faces = detect(path)
        faces_ += faces

    # 人物固定了（如果做更换脸型、发型可根据此改造）
    moulds_path = get_moulds_path(sex, major, degree)

    seamless_ims = process(faces_, moulds_path)

    img = join(seamless_ims)
    print(img)
    # img_with_background = load_background(img)
    img_with_background = Image.fromarray(img)

    # print(img_with_background)

    f = BytesIO()

    img_with_background.save(f, "png")

    return f

# 拼接图片
def join_img():

    paths = [ './static/images/head1.png', './static/images/top1.png', './static/images/bottom1.png']
    # img_array = ''
    # img = ''
    # for i, v in enumerate(paths):
    #     if i == 0:
    #         img = Image.open(v)  # 打开图片
    #         img_array = numpy.array(img)  # 转化为np array对象
    #     if i > 0:
    #         img_array2 = numpy.array(Image.open(v))
            
    #         img_array = numpy.concatenate((img_array, img_array2), axis=0)  # 纵向拼接
            
    #         print(img_array)
                
    # f = BytesIO()

    # img_array.save(f, "png")
    
    img1 = Image.open('./static/images/head1.png')  # 打开图片
    img2 = Image.open('./static/images/head1.png')  # 打开图片
    img3 = Image.open('./static/images/head1.png')  # 打开图片
    img_array1 = numpy.array(img1)  # 转化为np array对象
    img_array2 = numpy.array(img2)  # 转化为np array对象
    img_array3 = numpy.array(img3)  # 转化为np array对象
    
    print(img_array1.shape)
    print(img_array2.shape)
    print(img_array3.shape)
    img_result = numpy.concatenate((img_array1, img_array2, img_array3), axis=1)  # 纵向拼接
    
    img_result = Image.fromarray(img_result)
    
    f = BytesIO()
    img_result.save(f, "png")
    
    numpy.savetxt(f, img_result) # 只支持1维或者2维数组，numpy数组转化成字节流
    content = f.getvalue()  # 获取string字符串表示
    print(img_result)
    
    return content
