# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import View

from util.loginmixin import LoginMixin
from Salvation.settings import KEY, IV

from util.aes_decrypt_encrypt import AesDecryptEncrypt
from util.loggers import logger


# AES 加解密视图
class AesView(LoginMixin, View):


    def get(self, request):
        html_data = {
            "key": KEY,
            "iv": IV,
            'data': None,
            'code': None
        }
        if request.GET.get('data') is not None:
            try:
                submit = request.GET.get('submit')
                key = request.GET.get('key')
                iv = request.GET.get('iv')
                data = request.GET.get('data')

                html_data['key'] = key
                html_data['iv'] = iv

                aes = AesDecryptEncrypt(key, iv)

                if submit == '加密':
                    code = aes.encrypt(data)
                elif submit == '解密':
                    code = aes.decrypt(data)
                else:  # 解密
                    code = None
                    data = None
                    html_data['key'] = KEY
                    html_data['iv'] = IV

                html_data['data'] = data
                html_data['code'] = code

            except Exception as e:
                logger.error(f'解密异常！{e}')
            return render(request, 'tool/aes/aes_decrypt_encrypt.html', {"data": html_data})
        else:
            return render(request, 'tool/aes/aes_decrypt_encrypt.html', {"data": html_data})

