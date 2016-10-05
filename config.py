# -*- coding=utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))#首先获得当前文件（比如配置文件）所在的路径

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\x8bnoq\x82\xaa=\xa4\xdflS\x1a\xff\xf7k\xbb'
    SSL_DISABLE = True #是否重定向https
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True#?
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    FLASK_MAIL_SUBJECT_PREFIX = '[code闲谈]'
    FLASK_MAIL_SENDER = 'code ADMIN <420151940@qq.com>'
    FLASK_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASK_POSTS_PER_PAGE = 15
    FLASK_COMMENT_PER_PAGE = 20
    FLASK_FOLLOWERS_PER_PAGE = 20
    FLASK_SLOW_DB_QUERY_TIME = 0.5
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        #email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASK_MAIL_SENDER,
            toaddrs=[cls.FLASK_ADMIN],
            subject=cls.FLASK_MAIL_SUBJECT_PREFIX + 'Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class PlatformConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'platform': PlatformConfig,
    'default': DevelopmentConfig
}






