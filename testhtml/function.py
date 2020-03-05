# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 9:50
# @Author  : Yyf
# @FileName: function.py
# @Software: PyCharm
from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from django.http import FileResponse
import os
import combine3

def home(request):
    return render(request,'home.html')

def Upload(request):
    if request.method == "GET":
        name = request.GET.get(u'file')
        print(name)
        combine3.combine('stactic/'+name,'res')
        print(name.split('.'))
        name = name.split('.')[0]+'.docx'
        file = open('res/result_for_'+name, mode='rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s' % name
        return response
    if request.method == "POST":
        # 获取普通input标签值，即文件名
        # filname = request.POST.get('fileName')
        # 获取file类型的input标签值，即文件内容
        file = request.FILES.get('fileContent')
        filename = file.name
        print(filename)
        # 获取文件后缀名
        # postfix = file.name.split('.')[1]
        # 设置本地文件路径
        # file_path = os.path.join('static', filname + '.' + postfix)
        file_path ='stactic/'+ filename
        # 将上传的文件写入本地目录
        f = open(file_path, "wb")
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        print(filename)
        filename = str(filename)
        return render(request,"upload.html",{'filename':str(filename)})

def download(request):
    filename = request.GET.get(u'file')
    print(filename)
    name=filename.split('/')[1]
    file = open(filename,mode='rb')
    response=FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="%s'%name
    return response