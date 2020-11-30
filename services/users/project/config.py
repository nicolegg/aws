# services/users/project/config.py

import os


class BaseConfig:
    """Configuracion base"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_key'  # nuevo
    DEBUG_TB_ENABLED = False              # nuevo
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # nuevo
    BCRYPT_LOG_ROUNDS = 13


class DevelopmentConfig(BaseConfig):
    """Configuración de desarrollo"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    DEBUG_TB_ENABLED = True
    BCRYPT_LOG_ROUNDS = 4  # nuevo


class TestingConfig(BaseConfig):
    """Configuración de Testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    BCRYPT_LOG_ROUNDS = 4  # nuevo


class ProductionConfig(BaseConfig):
    """Configuración de producción"""
    DEBUG = False  # nuevo
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
