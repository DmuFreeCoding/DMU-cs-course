import os
import numpy as np
import cv2

# 定义图片尺寸
IMAGE_SIZE = 64


# 按照定义图像大小进行尺度调整
def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
    top, bottom, left, right = 0, 0, 0, 0
    # 获取图像尺寸
    h, w, _ = image.shape
    # 找到图片最长的一边
    longest_edge = max(h, w)
    # 计算短边需要填充多少使其与长边等长
    if h < longest_edge:
        d = longest_edge - h
        top = d // 2
        bottom = d // 2
    elif w < longest_edge:
        d = longest_edge - w
        left = d // 2
        right = d // 2
    else:
        pass
    # 设置填充颜色
    BLACK = [0, 0, 0]
    # 对原始图片进行填充操作
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)
    # 调整图像大小并返回
    return cv2.resize(constant, (height, width))


images, labels = list(), list()
# 读取训练数据
def read_path(path_name):
    for dir_item in os.listdir(path_name):
        # 合并成可识别的操作路径
        full_path = os.path.abspath(os.path.join(path_name, dir_item))
        # 如果是文件夹，则继续递归调用
        if os.path.isdir(full_path):
            read_path(full_path)
        else:
            if dir_item.endswith('.jpg'):
                # print(dir_item)
                image = cv2.imread(full_path)
                image = resize_image(image, IMAGE_SIZE, IMAGE_SIZE)
                images.append(image)
                labels.append(path_name)
    print(labels)
    return images, labels


# 从指定路径读取训练数据
def load_dataset(path_name):
    images, labels = read_path(path_name)
    # 由于图片是基于矩阵计算的， 将其转为矩阵
    images = np.array(images)
    print(images.shape)
    labels = np.array([0 if label.endswith('me') else 1 for label in labels])
    #print(labels)
    return images, labels


if __name__ == '__main__':
    images, labels = load_dataset("D:\data")
    print('裁剪完毕')