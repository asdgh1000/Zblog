from functools import wraps

import datetime
import jwt
import time
from flask import request, current_app
from enum import Enum, unique

from ..mongoDb import user as user_db


@unique
class AccountType(Enum):
    SUPER = 0
    COMMUNITY_ADMIN = 1
    NORMAL = 2


def __encode_auth_token(user_id, username, login_time):
    """
    生成认证Token
    :param user_id: int
    :param login_time: int(timestamp)
    :return: string
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
        'iat': datetime.datetime.utcnow(),
        'iss': 'ken',
        'data': {
            'id': user_id,
            'username': username,
            'login_time': login_time
        }
    }
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS256'
    ).decode('utf-8')


def __decode_auth_token(auth_token):
    """
    验证Token
    :param auth_token:
    :return: integer|string
    """
    # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
    # 取消过期时间验证
    payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'), options={'verify_exp': False})
    if 'data' in payload and 'id' in payload['data']:
        return payload
    else:
        raise jwt.InvalidTokenError('验证jwt失败')


def authenticate(username, password):
    """
    用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
    :param password:
    :return: json
    """
    user_info = user_db.auth_user(username, password)
    if user_info:
        login_time = int(time.time())
        user_db.update_user(user_info['_id'], {'login_time': login_time})
        return __encode_auth_token(str(user_info['_id']), username, login_time)
    else:
        raise Exception('认证失败')


def __parse_jwt():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise Exception('没有证书')

    auth_tokens = auth_header.split(" ")
    if not auth_tokens or auth_tokens[0] != 'JWT' or len(auth_tokens) != 2:
        raise jwt.InvalidTokenError('jwt token不能被正确的解析')
    else:
        auth_token = auth_tokens[1]
        payload = __decode_auth_token(auth_token)
    if isinstance(payload, str):
        raise jwt.InvalidTokenError('jwt token 不能被正确的解析')
    return payload


def identify(privilege):
    """
    用户鉴权
    :return: list
    """
    payload = __parse_jwt()
    user = user_db.get_user_by_id(payload['data']['id'])
    if user is None:
        raise jwt.InvalidTokenError('用户未找到')

    if user['login_time'] != payload['data']['login_time']:
        raise jwt.InvalidTokenError('权限验证失败')
    if privilege and ('type' not in user or privilege.value != user['type']):
        raise jwt.InvalidTokenError('权限验证失败')


def get_current_user_id():
    try:
        return __parse_jwt()['data']['id']
    except:
        return 'unknown'


def jwt_require(privilege=None):
    """
    检查管理员权限
    :param privilege: 
    :return: 
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            identify(privilege)
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def manage_privilege_check(fn):
    """
    检查用户是否具有修改对应小区的权限
    """

    @wraps(fn)
    def decorator(*args, **kwargs):
        if len(args) < 0:
            raise Exception("系统内部错误，请联系程序员")
        user_id = get_current_user_id()
        manage_communities = user_db.get_bind_manage_communities(user_id)
        # 修饰的函数的第一个参数必须是community_id
        community_id = kwargs['community_id']

        if community_id not in [str(x) for x in manage_communities]:
            raise Exception("没有管理该小区的权限")
        return fn(*args, **kwargs)

    return decorator
