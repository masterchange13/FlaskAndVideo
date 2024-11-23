"""
@Created by Mao on 2024/11/5
@Author:mao
@Github:https://github.com/masterchange13?tab=projects
@Gitee:https://gitee.com/master_change13
 
@File: test.py
@IDE: PyCharm
 
@Time: 2024/11/5 20:03
@Motto:不积跬步无以至千里，不积小流无以成江海，程序人生的精彩需要坚持不懈地积累！
@target: 大厂offer，高年薪

@@ written by GuangZhi Mao

@from:
@code target:
"""

import cv2

# video = cv2.VideoCapture(0)

# 假设 'video' 是一个已经打开的摄像头
video = cv2.VideoCapture('/dev/video0')


def set_image():
    # 从摄像头读取图像
    success, image = video.read()

    # 检查是否成功读取图像
    if not success:
        print("Failed to capture image")
        return

    # 将图像编码为 JPEG 格式（可选）
    ret, buffer = cv2.imencode('.jpg', image)

    # 保存图像到文件
    filename = "captured_image.jpg"  # 你想要保存的文件名
    cv2.imwrite(filename, image)  # 保存图像
    print(f"Image saved as {filename}")

def generate_frames():
    print("开始视频流...")
    while True:
            # 读取摄像头帧
            success, frame = video.read()
            if not success:
                print("未能读取帧，摄像头可能未打开或不存在。")
                break
            else:
                print("成功读取帧。")


def test():
    print("dddd")

if __name__ == '__main__':
    # generate_frames()
    # test()
    set_image()