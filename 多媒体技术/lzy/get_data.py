#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
def CatchPICFromVideo(catch_num, path_name):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # haarcascade_frontalface_alt2
    camera = cv2.VideoCapture(0+cv2.CAP_DSHOW)
    num = 0
    while True:
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        for (x, y, w, h) in faces:
            img_name = f'{path_name}/{str(num)}.jpg'
            image = frame[y:y + h, x:x + w]
            print(img_name)
            cv2.imwrite(img_name, image)
            num += 1
            if num > catch_num:
                break
            # 画出矩形框圈出人脸
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # 显示捕捉了多少张人脸
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f'num:{str(num)}', (x + 30, y + 30), font, 1, (255, 0, 255), 4)
        if num > catch_num:
            break
        # 显示图像
        cv2.imshow('camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    CatchPICFromVideo(1000 ,'D:\data\others')