import tensorflow.keras as keras
import cv2
IMAGE_SIZE=64
#裁剪照片得到64*64的尺寸
def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
    top, bottom, left, right = (0, 0, 0, 0)

    # 获取图像尺寸
    h, w, _ = image.shape

    # 对于长宽不相等的图片，找到最长的一边
    longest_edge = max(h, w)

    # 计算短边需要增加多上像素宽度使其与长边等长
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass

        # RGB颜色
    BLACK = [0, 0, 0]
    # 给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)
    # 调整图像大小并返回
    return cv2.resize(constant, (height, width))
##########预测函数########################
def face_predict(image,model):
    image = resize_image(image)
    image = image.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))
    image=image.astype('float32')
    image/=255
    # 给出输入属于各个类别的概率与误差
    result = model.predict_proba(image)
    print('属于该类的概率与误差是:', result)

    # 给出类别预测：0或者1
    result = model.predict_classes(image)

    # 返回类别预测结果
    return result[0]

####如果带不动就展示这个程序咯
if __name__ == '__main__':
    # 加载模型
    my_model = keras.models.load_model('D:\model\model.h5')

    # 框住人脸的矩形边框颜色
    color = (0, 255, 0)

    # 捕获指定摄像头的实时视频流
    camera = cv2.VideoCapture(0)

    # 人脸识别分类器本地存储路径
    cascade_path = "/anaconda3/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"

    # 循环检测识别人脸
    while True:
        ret, frame = camera.read()  # 读取一帧视频

        # 图像灰化，降低计算复杂度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 使用人脸识别分类器，读入分类器
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # 利用分类器识别出哪个区域为人脸
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # 截取脸部图像提交给模型识别这是谁
                image = frame[y: y + h, x: x + w]
                faceID = face_predict(image,my_model)

                # 如果是“我”
                if faceID == 0:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness=2)

                    # 文字提示是谁
                    cv2.putText(frame, 'me',
                                (x + 30, y + 30),  # 坐标
                                cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                                1,  # 字号
                                (255, 0, 255),  # 颜色
                                2)  # 字的线宽
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness=2)

                    # 文字提示是谁
                    cv2.putText(frame, 'others',
                                (x + 30, y + 30),  # 坐标
                                cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                                1,  # 字号
                                (255, 0, 255),  # 颜色
                                2)

        cv2.imshow("camera", frame)

        # 等待1毫秒看是否有按键输入
        k = cv2.waitKey(1)
        # 如果输入q则退出循环
        if k & 0xFF == ord('q'):
            break

    # 释放摄像头并销毁所有窗口
    camera.release()
    cv2.destroyAllWindows()