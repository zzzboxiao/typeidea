from .base import *



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea',      # 数据库名称
        'HOST': '127.0.0.1',     # 数据库地址，本机 ip 地址 127.0.0.1 
        'PORT': 3306,            # 端口 
        'USER': 'root',          # 数据库用户名
        'PASSWORD': '88156088',  # 数据库密码
    }
}