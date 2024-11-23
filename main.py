"""
@Created by Mao on 2024/11/5
@Author:mao
@Github:https://github.com/masterchange13?tab=projects
@Gitee:https://gitee.com/master_change13
 
@File: main.py
@IDE: PyCharm
 
@Time: 2024/11/5 19:39
@Motto:不积跬步无以至千里，不积小流无以成江海，程序人生的精彩需要坚持不懈地积累！
@target: 大厂offer，高年薪

@@ written by GuangZhi Mao

@from:
@code target:
"""
import flask
from flask import Flask, jsonify, request, send_file, Response
import cv2
from PIL import Image
import io

# 打开摄像头（0 表示默认摄像头）
# camera = cv2.VideoCapture('/dev/video0')
# print(camera)

app = Flask(__name__)


# 根路由
@app.route("/")
def hello():
    return flask.render_template("home.html")


# 获取带参数的路由
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    query_param = request.args.get("q")
    return jsonify({"item_id": item_id, "query": query_param})


# 使用 POST 请求创建新项
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    return jsonify({"name": name, "price": price}), 201


@app.route("/image", methods=["GET"])
def get_image():
    image = Image.open("./1.jpeg")

    # 将图片保存到字节流中
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)

    # 使用 send_file 返回图片
    return send_file(img_io, mimetype='image/jpeg')


@app.route("/image2", methods=["GET"])
def get_image2():
    return send_file('./2.jpeg')


@app.route("/video", methods=["GET"])
def get_video():
    return send_file('3.mp4', mimetype="video/mp4")


@app.route("/video2", methods=["GET"])
def get_video2():
    return send_file('3.mp4', mimetype="video/mp4")




def generate_frames():
    camera = cv2.VideoCapture('/dev/video0')
    print("开始视频流...")
    while True:
        try:
            # 读取摄像头帧
            success, frame = camera.read()
            if not success:
                print("未能读取帧，摄像头可能未打开或不存在。")
                break
            else:
                # print("成功读取帧。")

                # 将帧转换为 JPEG 格式
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    print("帧编码失败。")
                    continue  # 如果编码失败，继续下一个循环

                frame = buffer.tobytes()

                # 使用 yield 逐帧返回
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        except Exception as e:
            print(f"捕获到异常: {e}")
            break  # 根据需要，可以选择继续或退出


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.teardown_appcontext
# def close_camera(exception):
#     """释放摄像头资源"""
#     if camera.isOpened():
#         camera.release()

@app.route('/videopage')
def camera_page():
    return flask.render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
