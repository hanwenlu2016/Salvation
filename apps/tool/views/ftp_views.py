# -*- coding: utf-8 -*-
import os

from django.http import FileResponse
from django.shortcuts import render
from django.views import View

from util.loginmixin import LoginMixin

from util.ftp_download import FtpDownload, zipDir, replace_char
from util.loggers import logger
from Salvation.settings import FTP_PATH


# ftp 下载视图
class FtpView(LoginMixin, View):

    def get(self, request):

        try:
            ftp_host = request.GET.get('ftp_host')
            ftp_port = request.GET.get('ftp_port')
            ftp_name = request.GET.get('ftp_name')
            ftp_pwd = request.GET.get('ftp_pwd')
            ftp_file = request.GET.get('ftp_file')

            if ftp_host and ftp_port and ftp_name and ftp_pwd and ftp_file is not None:
                # 兼容路径以/结尾
                if isinstance(ftp_file, str) and ftp_file[-1] == '/':
                    ftp_file = replace_char(ftp_file, '', -1)
                # 登录ftp
                ftp = FtpDownload(ftpserver=ftp_host, port=int(ftp_port), usrname=ftp_name, pwd=ftp_pwd)
                filename = ftp_file.split('/')[-1]  # 一般为文件

                if '.' in filename:  # 单一文件下载
                    dowmload_path = ftp.independentDownload(ftp_file)

                    try:
                        if dowmload_path:
                            response = FileResponse(open(dowmload_path, 'rb'))
                            response['Content-Type'] = 'application/octet-stream'
                            response['Content-Disposition'] = 'attachment;filename={}'.format(filename)
                            return response
                    except Exception as e:
                        logger.error(e)
                        msg = {'msg': '下载文件时发生了异常，请稍后在尝试！！！'}
                        return render(request, 'tool/ftp/ftp_download.html', msg)

                else:
                    dowmload_paths = ftp.downloadFiles(ftp_file)  # 下载ftp到本地
                    dowmload_zip = zipDir(dowmload_paths, f'{filename}.zip')  # 压缩本地文件

                    try:
                        if dowmload_paths:
                            response = FileResponse(open(dowmload_zip, 'rb'))
                            response['Content-Type'] = 'application/octet-stream'
                            response['Content-Disposition'] = 'attachment;filename={}.zip'.format(filename)
                            if os.path.exists(dowmload_zip):
                                os.remove(dowmload_zip)
                            return response
                    except Exception as e:
                        logger.error(e)
                        msg = {'msg': '下载文件时发生了异常，请稍后在尝试！！！'}
                        return render(request, 'tool/ftp/ftp_download.html', msg)
            return render(request, 'tool/ftp/ftp_download.html', )
        except Exception as e:
            logger.error(f'下载文件异常！{e}')
            msg = {'msg': '下载文件异常请稍后在尝试！！！'}
            return render(request, 'tool/ftp/ftp_download.html', msg)


# ftp 下载工具视图
class FtpToolView(LoginMixin, View):

    def get(self, request):

        try:
            abspath = os.path.abspath('.')  # 当前目录的上上级目录
            ftptool_path = abspath + FTP_PATH  # 拼接路径

            response = FileResponse(
                open(ftptool_path, 'rb'))

            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename={}'.format('FTPtool.zip')
            return response
        except Exception as e:
            logger.error(e)
            msg = {'msg': '下载工具异常请稍后在尝试！！！'}
            return render(request, 'tool/ftp/ftp_download.html', msg)
