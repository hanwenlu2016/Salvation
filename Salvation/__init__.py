import pymysql
from .celery import app as celery_app

# 连接mysql 排除版本错误
pymysql.version_info = (1, 4, 14, "final", 0)

pymysql.install_as_MySQLdb()
__all__ = ('celery_app',)