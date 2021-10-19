# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import View

from util.loginmixin import LoginMixin
from Salvation.settings import KEY, IV

from util.aes_decrypt_encrypt import AesDecryptEncrypt
from util.loggers import logger


# AES 加解密视图
class AesView(LoginMixin, View):
    data = {
        "key": KEY,
        "iv": IV,
        'data': None,
        'code': None
    }

    def get(self, request):
        return render(request, 'tool/aes/aes_decrypt_encrypt.html', {"data": self.data})

    def post(self, request):
        try:
            submit = request.POST.get('submit')
            if submit=='加密':

                key = request.POST.get('key')
                iv = request.POST.get('iv')
                data = request.POST.get('data')
                aes = AesDecryptEncrypt(key, iv)
                code = aes.encrypt(data)
                self.data['data'] = data
                self.data['code'] = code
            else:  #解密
                key = request.POST.get('key')
                iv = request.POST.get('iv')
                data = request.POST.get('data')
                aes = AesDecryptEncrypt(key, iv)
                code = aes.decrypt(data)
                self.data['data'] = data
                self.data['code'] = code
        except Exception as e:
            logger.error(f'解密异常！{e}')

        return render(request, 'tool/aes/aes_decrypt_encrypt.html', {"data": self.data})
        # return render(request, 'tool/aes/aes_decrypt_encrypt.html', {"data": data})
