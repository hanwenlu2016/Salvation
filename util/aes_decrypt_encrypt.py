# -*- coding: utf-8 -*-


import base64
from Crypto.Cipher import AES




class AesDecryptEncrypt:
    """
    AES 加解密类
    """

    def __init__(self, key, iv):
        self.key = key  # 密钥（key） --CBC模式加密
        self.iv = iv    # 偏移量（iv）

    def decrypt(self, decrypt_data):
        """
        解密函数
        :param decrypt_data:  需要解密函数参数
        :return:
        """

        # 将解密数据转换位bytes类型数据
        data = decrypt_data.encode('utf8')
        encodebytes = base64.decodebytes(data)

        # 补位数据
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.iv.encode('utf8'))
        text_decrypted = cipher.decrypt(encodebytes)
        unpad = lambda s: s[0:-s[-1]]
        text_decrypted = unpad(text_decrypted)

        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted

    def encrypt(self, encrypt_data):
        """
        加密函数
        :param encrypt_data: 需要的加密参数
        :return:
        """
        # # 字符串补位
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        data = pad(encrypt_data)

        # 加密后得到的是bytes类型的数据
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.iv.encode('utf8'))
        encryptedbytes = cipher.encrypt(data.encode('utf8'))

        # 使用Base64进行编码,返回byte字符串 并对字符串按utf-8进行解码
        encodestrs = base64.b64encode(encryptedbytes).decode('utf8')

        return encodestrs
#

# if __name__ == '__main__':
#     KEY = 'rk.=278ZAmb~0&]F'
#     IV = '1dd89`X3nVfmchm?'
#     aes = AesDecryptEncrypt(KEY,IV)
#     e = aes.encrypt('fda_App*8')  # 加密
#     d = aes.decrypt('SzNuqN2nDkXzJzXTMYR1iQ==')  #解密
#     print(e)
#     print(d)
