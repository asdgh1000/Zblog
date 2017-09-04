from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class

from config import config
import json
from flask_pymongo import ObjectId
import datetime

mail = Mail()
mongo = PyMongo()
photos = UploadSet('photos', IMAGES)
redis_store = FlaskRedis()

# 跨域
cors = CORS()


# 处理mongodb ObjectId类型
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def create_app(config_name):
    app = Flask(__name__)
    app.json_encoder = JSONEncoder
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mail.init_app(app)
    mongo.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)
    cors.init_app(app)
    redis_store.init_app(app)

    from .api_v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint)
    return app
