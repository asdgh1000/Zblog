import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    #随机生成的字符串
    SECRET_KEY = '\xdfq\xad\xa8\rR\xbf\xbe\x19m^q\xcd\x1a\xf8+\x11\x9f\xb5e\x8e\xd6\x1d\xa5'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    #邮件配置
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'photos')

    #redis做session
    # 默认本地redis
    SESSION_TYPE = 'redis'
    SESSION_KEY_PREFIX = 'sess-key:'
    SESSION_USE_SIGNER = True
    # session失效时间是15天
    PERMANENT_SESSION_LIFETIME = 15 * 24 * 3600


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    #数据库配置
    MONGO_HOST = 'localhost'
    # MONGO_PORT = 27017
    # MONGO_USERNAME = 'bigcAdmin'
    # MONGO_PASSWORD = '1234Abcd'
    MONGO_DBNAME = 'yjll_db'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    #数据库配置
    MONGO_DBNAME = 'yjll_db'


class ProductionConfig(Config):
    MONGO_HOST = '172.16.190.86'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'yjll-db-web'
    MONGO_PASSWORD = 'yjll-db-web-passwd-54321'
    MONGO_DBNAME = 'yjll_db'
    MONGO_CONNECT = False


config = {
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
