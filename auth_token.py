"""
@Created by Mao on 2024/12/1
@Author:mao
@Github:https://github.com/masterchange13?tab=projects
@Gitee:https://gitee.com/master_change13
 
@File: auth_token.py
@IDE: PyCharm
 
@Time: 2024/12/1 20:01
@Motto:不积跬步无以至千里，不积小流无以成江海，程序人生的精彩需要坚持不懈地积累！
@target: 大厂offer，高年薪

@@ written by GuangZhi Mao

@from:
@code target:
"""

# from flask import Flask, request, jsonify
import jwt
import datetime

SECRET_KEY = 'zyq'

# 生成 Token
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24*360)  # 设置过期时间
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# 验证 Token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
