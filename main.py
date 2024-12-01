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
import os

# token
from auth_token import *

# 打开摄像头（0 表示默认摄像头）
# camera = cv2.VideoCapture('/dev/video0')
# print(camera)

app = Flask(__name__)

# 全局请求钩子
@app.before_request
def before_request():
    # 排除不需要 Token 验证的路由
    if request.endpoint in ['login', 'video_feed']:
        return  # 跳过这些路由的验证

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Token missing'}), 401

    if not auth_header.startswith("Bearer "):
        print(f"Invalid auth header format: {auth_header}")  # 记录日志
        return jsonify({'error': 'Token invalid format, should start with "Bearer "'}), 401

    # 提取 Token
    token_parts = auth_header.split(" ")
    if len(token_parts) != 2:
        return jsonify({'error': 'Token invalid format'}), 401

    token = token_parts[1]

    # 验证 Token
    result = verify_token(token)
    if 'error' in result:
        print(f"Token verification failed: {result['error']}")  # 记录日志
        return jsonify(result), 401


# 根路由
@app.route("/")
def hello():
    return flask.render_template("home.html")

# 登录路由
@app.route("/login", methods=['POST'])
def login():
    # 从 JSON 数据中提取参数
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # 检查用户名和密码
    if username == 'zyq' and password == '030701':
        # 如果登录成功，生成 JWT Token
        token = generate_token(username)
        return jsonify(success=True, token=token), 200
    else:
        return jsonify(success=False, message="Invalid username or password"), 400

# 受保护路由
@app.route('/protected', methods=['GET'])
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Token missing or invalid format'}), 401
    token = auth_header.split(" ")[1]

    # 验证 Token
    result = verify_token(token)
    if not result['success']:
        return jsonify(result), 401
    return jsonify({'message': 'Access granted', 'data': result['data']})

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


# in order to test cross core
@app.route('/test')
def test():
    return "this is test"


# file transfer
# 设置文件上传的目录
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 确保目录存在

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}  # 可以根据需求添加其他类型

# 检查文件扩展名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:  # 检查请求中是否有文件
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']  # 获取文件

    if file.filename == '':  # 检查文件名是否为空
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):  # 检查文件是否允许上传
        filename = file.filename

        # 检查文件是否已存在
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            return jsonify({'error': 'File already exists'}), 400

        file.save(filepath)  # 保存文件到指定目录
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
