import pymysql

# 连接mysql 排除版本错误
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()
