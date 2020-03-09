# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 9:50
# @Author  : Yyf
# @FileName: function.py
# @Software: PyCharm
import os
import random
import time
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.utils.http import urlquote

import combine3

from Crypto.Cipher import DES
from binascii import b2a_hex, a2b_hex


class MyDESCrypt:  # 自己实现的DES加密类
    def __init__(self, key=''):
        # 密钥长度必须为64位，也就是8个字节
        if key is not '':
            self.key = key.encode('utf-8')
        else:
            self.key = '6biknow6'.encode('utf-8')
        self.mode = DES.MODE_CBC

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        try:
            text = text.encode('utf-8')
            cryptor = DES.new(self.key, self.mode, self.key)
            # 这里密钥key 长度必须为16（DES-128）,
            # 24（DES-192）,或者32 （DES-256）Bytes 长度
            # 目前DES-128 足够目前使用
            length = 16  # lenth可以设置为8的倍数
            count = len(text)
            if count < length:
                add = (length - count)
                # \0 backspace
                # text = text + ('\0' * add)
                text = text + ('\0' * add).encode('utf-8')
            elif count > length:
                add = (length - (count % length))
                # text = text + ('\0' * add)
                text = text + ('\0' * add).encode('utf-8')
            self.ciphertext = cryptor.encrypt(text)
            # 因为DES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
            # 所以这里统一把加密后的字符串转化为16进制字符串
            return b2a_hex(self.ciphertext)
        except:
            return ""

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        try:
            cryptor = DES.new(self.key, self.mode, self.key)
            plain_text = cryptor.decrypt(a2b_hex(text))
            # return plain_text.rstrip('\0')
            return bytes.decode(plain_text).rstrip('\0')
        except:
            return ""

def home(request):
    return render(request, 'home.html')

def Upload(request):
    if request.method == "GET":
        en_name = request.GET.get(u'file')
        #对应没有参数传入的情况
        if not en_name:
             return render(request, 'home.html')
        des = MyDESCrypt()
        _name = des.decrypt(bytes(en_name, encoding="utf-8"))
        filename, rename = _name.split('/')
        res_dir = 'res/'
        combine3.combine(os.path.join('upload/', rename), res_dir)
        # 解析完成的结果文件
        res_doc = os.path.join(res_dir, 'result_for_' + rename.split('.')[0] + '.docx')
        # 下载的时候对应的文件名
        if len(filename) == 255:
            # 进行文件名缩短
            tmp = filename.split('.')[0][:-1]
            dis_name =tmp + '.docx'
        else:
            dis_name = filename.split('.')[0] + '.docx'

        file = open(res_doc, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s' % urlquote(dis_name)
        return response

    if request.method == "POST":
        file_stream = request.FILES.get('fileContent')
        if not file_stream:
            return render(request, "home.html", {'msg': '您没有上传任何pdf文件'})
        filename = str(file_stream.name)
        if not filename.endswith('.pdf'):
            return render(request, "home.html", {'msg': '请上传pdf文件, %s不是pdf文件 '% filename})
        rename = _save(filename, file_stream)
        _name = filename + '/' + rename
        des = MyDESCrypt()
        en_name = des.encrypt(_name)
        return render(request, "upload.html", {'filename': str(en_name, encoding='utf-8'), 'msg':'请点击下载文献解析后的文件，解析需要片刻时间请您耐心等待'})


def download(request):
    filename = request.GET.get(u'file')
    name = filename.split(os.path.sep)[1]
    file = open(filename, mode='rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s' % name
    return response


def _save(name, file_stream):
    # name为上传文件名称
    # 文件扩展名
    ext = os.path.splitext(name)[1]
    # 定义文件名，年月日时分秒随机数
    fn = time.strftime('%Y%m%d%H%M%S')
    fn = fn + '_%d' % random.randint(0, 100)
    rename = fn + ext
    upload_dir = 'upload/'
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    file_path = os.path.join(upload_dir, rename)
    # 将上传的文件写入本地目录
    f = open(file_path, "wb")
    for chunk in file_stream.chunks():
        f.write(chunk)
    f.close()
    return rename