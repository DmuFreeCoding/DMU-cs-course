""" 从视频读取帧保存为图片"""
import cv2
import numpy as np
#cap = cv2.VideoCapture("C:/Users/lenovo/Videos/1.mp4")#读取文件
cap = cv2.VideoCapture(0)#读取摄像头

#皮肤检测
def A(img):

    YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB) #转换至YCrCb空间
    (y,cr,cb) = cv2.split(YCrCb) #拆分出Y,Cr,Cb值
    cr1 = cv2.GaussianBlur(cr, (5,5), 0)
    _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Ostu处理
    res = cv2.bitwise_and(img,img, mask = skin)
    return res

def B(img):

    #binaryimg = cv2.Canny(Laplacian, 50, 200) #二值化，canny检测
    h = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #寻找轮廓
    contour = h[0]
    contour = sorted(contour, key = cv2.contourArea, reverse=True)#已轮廓区域面积进行排序
    #contourmax = contour[0][:, 0, :]#保留区域面积最大的轮廓点坐标
    bg = np.ones(dst.shape, np.uint8) *255#创建白色幕布
    ret = cv2.drawContours(bg,contour[0],-1,(0,0,0),3) #绘制黑色轮廓
    return ret


while(True):

    ret, frame = cap.read()
    #下面三行可以根据自己的电脑进行调节
    src = cv2.resize(frame,(400,350), interpolation=cv2.INTER_CUBIC)#窗口大小
    cv2.rectangle(src, (90, 60), (300, 300 ), (0, 255, 0))#框出截取位置
    roi = src[60:300 , 90:300]  # 获取手势框图

    res = A(roi)  # 进行肤色检测
    cv2.imshow("0",roi)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    dst = cv2.Laplacian(gray, cv2.CV_16S, ksize = 3)
    Laplacian = cv2.convertScaleAbs(dst)

    contour = B(Laplacian)#轮廓处理
    cv2.imshow("2",contour)

    key = cv2.waitKey(50) & 0xFF
    if key == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()