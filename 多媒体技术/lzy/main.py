#导入相关包
import PySimpleGUI as sg
import numpy as np
import cv2
from predict import *
# 打开内置摄像头
cap = cv2.VideoCapture(0)
# 背景色
sg.theme('Reddit')
# 定义窗口布局，创建不同功能的按钮
layout = [
    [sg.Image(filename='', key='image')],
    [sg.Radio('默认状态', 'Radio', True, size=(10, 1))],
    [sg.Radio('阈值二值化', 'Radio', size=(10, 1), key='thresh'),
     sg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='thresh_slider')],
    [sg.Radio('边缘检测', 'Radio', size=(10, 1), key='canny'),
     sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='canny_slider_a'),
     sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='canny_slider_b'),
     sg.Checkbox('加入降噪',key='gass'),
     ],
    [sg.Radio('轮廓检测', 'Radio', size=(10, 1), key='contour'),
     sg.Slider((0, 255), 127, 1, orientation='h', size=(40, 15), key='base_slider')],
    [sg.Radio('高斯滤波', 'Radio', size=(10, 1), key='blur'),
     sg.Slider((1, 11), 1, 1, orientation='h', size=(40, 15), key='blur_slider'),
     sg.Checkbox('线性滤波', key='line'),
     ],
    [sg.Radio('色彩转换', 'Radio', size=(10, 1), key='hue'),
     sg.Slider((0, 225), 0, 1, orientation='h', size=(40, 15), key='hue_slider')],
    [sg.Radio('调节对比度', 'Radio', size=(10, 1), key='enhance'),
     sg.Slider((1, 255), 128, 1, orientation='h', size=(40, 15), key='enhance_slider')],
    [sg.Radio('人脸识别','Radio',size=(10,1),key='face'), sg.Radio('笑脸识别','Radio',size=(10,1),key='smile')],
    [sg.Radio('强化识别','Radio',size=(10,1),key='Big')],
    [sg.Button('Exit', size=(10, 1))]
]
# 窗口设计
window = sg.Window('实时图像处理系统',
                   layout,
                   location=(500, 500),
                   finalize=True,
                   font='宋体',
                   )
# 导入识别模型
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
##主体部分
while True:
    event, values = window.read(timeout=0, timeout_key='timeout')
    # 实时读取图像,逐帧捕获
    ret, frame = cap.read()
    ###########阈值二分类#############
    if values['thresh']:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #该函数有两个输出，只取第二个，为阈值之后的图像
        frame = cv2.threshold(frame, values['thresh_slider'], 255, cv2.THRESH_BINARY)[1]
    ###########边缘检测#############
    if values['canny']:
        if values['gass']:
            # 加入降噪
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
        #不加入降噪
        frame = cv2.Canny(frame, values['canny_slider_a'], values['canny_slider_b'])
    ###########轮廓检测#############
    if values['contour']:
        #需要先转化为二值图
        gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray=cv2.threshold(gray,values['base_slider'],255,cv2.THRESH_BINARY)[1]
        #21维的高斯滤波降噪
        hue = cv2.GaussianBlur(gray, (21, 21), 1)
        #三个参数，输入图像、层次类型、轮廓逼近方法，第一个返回值为修改后的图像，也就是轮廓
        cnts = cv2.findContours(hue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        #绘制轮廓,cnt为存储了多个轮廓的数组，color代表线条的颜色，
        cv2.drawContours(frame, cnts, -1, (0, 0, 255), 3)
    ###########轮廓检测#############
    if values['blur']:
        #高斯滤波
        frame = cv2.GaussianBlur(frame, (21, 21), values['blur_slider'])
        if values['line']:
            kernel=np.ones((5,5),np.float32)/25
            frame=cv2.filter2D(frame,-1,kernel)
    ###########颜色转换#############
    if values['hue']:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        frame[:, :, 0] += int(values['hue_slider'])
        #再映射回RGB空间
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    ###########调节对比度#############
    if values['enhance']:
        ##得到一个提高度
        enh_val = values['enhance_slider'] / 40
        #直方图均衡化的函数进行实例化，选择（8,8）的网格
        clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        #将这个函数应用到当前图像上，得到最终图像
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    ###########人脸识别##################
    if values['face']:
        #导入分类函数，找到人脸的大致位置
        faces = face_cascade.detectMultiScale(frame, 1.3, 2)
        for (x, y, w, h) in faces:
            # 画出人脸框，蓝色，画笔宽度微
            face = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # 框选出人脸区域，在人脸区域而不是全图中进行人眼检测，节省计算资源
            face_area = face[y:y + h, x:x + w]
            ## 人眼检测
            # 用人眼级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
            eyes = eye_cascade.detectMultiScale(face_area, 1.3, 10)
            for (ex, ey, ew, eh) in eyes:
                # 画出人眼框，绿色，画笔宽度为1
                cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
    ###########笑脸识别############
    if values['smile']:
        faces = face_cascade.detectMultiScale(frame, 1.3, 2)
        for (x, y, w, h) in faces:
            face = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face_area = face[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(face_area, 1.3, 10)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
                ## 微笑检测
                # 用微笑级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
                smiles = smile_cascade.detectMultiScale(face_area, scaleFactor=1.16, minNeighbors=65, minSize=(25, 25),
                                                        flags=cv2.CASCADE_SCALE_IMAGE)
                for (ex, ey, ew, eh) in smiles:
                    # 画出微笑框，红色（BGR色彩体系），画笔宽度为1
                    cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 1)
                    cv2.putText(frame, 'Smile', (x, y - 7), 3, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
    ############强化版人脸识别#################
    if values['Big']:
        #初始化模型
        my_model = keras.models.load_model('D:\model\model.h5')
        #转化为灰度图像
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # 利用分类器识别出哪个区域为人脸
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # 截取脸部图像提交给模型识别这是谁
                image = frame[y: y + h, x: x + w]
                faceID = face_predict(image, my_model)

                # 如果是“我”
                if faceID == 0:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
                    # 文字提示是谁
                    cv2.putText(frame, 'me',
                                (x + 30, y + 30),  # 坐标
                                cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                                1,  # 字号
                                (255, 0, 255),  # 颜色
                                2)  # 字的线宽
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
                    # 文字提示是谁
                    cv2.putText(frame, 'others',
                                (x + 30, y + 30),  # 坐标
                                cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                                1,  # 字号
                                (255, 0, 255),  # 颜色
                                2)
    """    
    暂时停止使用的功能，因为太卡了
    if values['finger']:
        skinCrCbHist = np.zeros((256, 256), dtype=np.uint8)
        cv2.ellipse(skinCrCbHist, (113, 155), (23, 25), 43, 0, 360, (255, 255, 255), -1)  # 绘制椭圆弧线
        YCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)  # 转换至YCrCb空间
        (y, Cr, Cb) = cv2.split(YCrCb)  # 拆分出Y,Cr,Cb值
        skin = np.zeros(Cr.shape, dtype=np.uint8)  # 掩膜
        (x, y) = Cr.shape
        for i in range(0, x):
            for j in range(0, y):
                if skinCrCbHist[Cr[i][j], Cb[i][j]] > 0:  # 若不在椭圆区间中
                    skin[i][j] = 255
        frame= cv2.bitwise_and(frame, frame, mask=skin)"""
    if event == 'Exit' or event is None:
        break
    # GUI实时更新，捕捉当前图像，然后转化为byte形式
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    # 更新图像
    window['image'].update(data=imgbytes)
#关闭GUI界面
window.close()
