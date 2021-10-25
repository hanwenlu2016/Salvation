# -*- coding: utf-8 -*-

import os
import zipfile
from ftplib import FTP

from util.loggers import logger


def replace_char(string, char, index):
    """
    替换字符串中指定位置字符
    :param string: 字符串
    :param char: 需要替换的字符串
    :param index: 索引
    :return:
    """
    string = list(string)
    string[index] = char
    return ''.join(string)


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()
    return  os.path.join(os.path.abspath('.'),outFullName)

class FtpDownload:
    """
    ftp 下载类
    """

    def __init__(self, ftpserver: str or int, usrname: str or int, pwd: str or int, port: int = 21):
        self.ftpserver = ftpserver  # ftp主机IP
        self.port = port  # ftp端口
        self.usrname = usrname  # 登陆用户名
        self.pwd = pwd  # 登陆密码
        self.ftp = self.ftpConnect()

    def ftpConnect(self) -> None:
        """
        # ftp连接
        :return:
        """
        ftp = FTP()
        try:
            ftp.connect(self.ftpserver, self.port)
            ftp.login(self.usrname, self.pwd)
        except:
            logger.error('FTP login failed!!!')
            raise IOError('\n FTP login failed!!!')
        else:
            logger.info(ftp.getwelcome())
            logger.info('FTP connection successful!!!')
            return ftp

    # 单个文件下载到本地
    def independentDownload(self, ftpfile):
        """
        文件下载
        :param ftpfile:
        :param localfile:
        :return:
        """

        localpath = self.get_photo_path(multiple=False)  # 生成临时目录

        if not os.path.exists(localpath):  # 如果生成临时目录不存在就创建
            os.makedirs(localpath)

        # # 临时目录拼接下载名称
        tmpdir = ftpfile.split('/')[-1]
        file_path = os.path.join(localpath, tmpdir)

        try:
            bufsize = 1024
            with open(file_path, 'wb') as fid:
                self.ftp.retrbinary('RETR {0}'.format(ftpfile), fid.write, bufsize)
            return file_path
        except Exception as e:
            logger.error(e)
            pass

    # 配合批量下载
    def downloadFile(self, ftpfile: str, filename) -> bool or None:
        """
        文件下载
        :param ftpfile: 远程目录
        :param localfile: 下载成功后的文件
        :return:
        """

        try:
            bufsize = 1024
            with open(filename, 'wb') as fid:
                self.ftp.retrbinary('RETR {0}'.format(ftpfile), fid.write, bufsize)
            return True
        except Exception as e:
            logger.error(e)
            pass

    # 批量下载
    def downloadFiles(self, ftpath: str) -> str:
        """
        下载批量
        :param ftpath: 远程目录路径
        :return:
        """

        tmpdir = ftpath.split('/')[-1]  # 临时目录取下载路径的最后一个目录名称
        localpath = self.get_photo_path(tmpdir=tmpdir)  # 拼接临时目录

        if not os.path.exists(localpath):  # 如果目录不存在就创建
            os.makedirs(localpath)

        logger.info('FTP PATH: {0}'.format(ftpath))

        try:

            logger.info('----------- downloading!!!')
            self.ftp.cwd(ftpath)

            for i, file in enumerate(self.ftp.nlst()):
                logger.info('{0} <> {1}'.format(i, file))
                local = os.path.join(localpath, file)

                if os.path.isdir(file):  # 判断是否为子目录
                    self.downloadFiles(file)
                else:
                    self.downloadFile(file, local)

            self.ftp.cwd('..')
            self.ftp.quit()
            return localpath

        except Exception as e:
            logger.error(e)
            pass

    def get_photo_path(self, tmpdir=None, multiple=True):
        """
        动态生成文件目录
        :param tmpdir: 零时目录
        :return:
        """
        curren_dir = os.path.abspath('.')  # 当前目录的上上级目录 实际返回调用视图的上层

        files = 'upload/ftptmp'  # 固定路径

        if multiple:
            if tmpdir is not None:
                return f'{curren_dir}/{files}/{tmpdir}'
            else:
                logger.info('缺少 tmpdir 参数')
                return '缺少 tmpdir 参数'
        else:
            return f'{curren_dir}/{files}'

    # 退出FTP连接
    def ftpDisConnect(self) -> None:
        self.ftp.quit()


# # 程序入口
#if __name__ == '__main__':
    #ftpath = '/pdb/send/ZBAA/SCHD/ADFT/2021/08/18'  # 远程目录
    #ftpath = '/pdb/send/ZBAA/SCHD/ADFT/2021/08/18'
    #ftpath_flies = '/pdb/send/ZBAA/SCHD/ADFT/2021/08/18/ADFT_9117_20210818000031.xml'  # 远程文件

    #Ftp = FtpDownload('192.168.7.95', 'pdb', 'pdb')

    #Ftp.downloadFile('/pdb/send/ZBAA/SCHD/ADFT/2021/08/18/ADFT_9117_20210818000031.xml', 'ADFT_9117.xml')  # 单个文件下载

    #x = Ftp.downloadFiles(ftpath)  # 批量下载
    #print(x)
# print(x)
#     z = Ftp.independentDownload(ftpath_flies)
#     print(z)