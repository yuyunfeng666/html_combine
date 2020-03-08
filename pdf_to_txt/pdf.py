#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time    : 2019/12/17 15:16
@Author  : BioKnowZG
@File    : pdf.py
@Software: PyCharm
"""
import os, re
import shutil
from io import StringIO
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTRect, LTFigure
from pdfminer.pdfinterp import PDFResourceManager, process_pdf, PDFPageInterpreter, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

from .utils import crop_img, makedir_if_not_exist
from .utils import is_author


def get_files():
    '''
    获取data文件夹下面的目录
    :return: 文件目录的绝对路径
    '''
    root_path = os.path.dirname(__file__)
    data_path = os.path.join(root_path, 'data')
    pdf_files = []
    for root, dirs, files in os.walk(data_path):
        pdf_files.extend([os.path.join(data_path, file) for file in files if file.endswith('.pdf')])
    return pdf_files


def read_pdf(file_path):
    '''
    读取pdf文件
    :param pdf: pdf路径
    :return: 返回的是pdf的解析后的结果
    '''
    # resource manager
    pdf = open(file_path, "rb")
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    # 获取所有行
    content = str(content)
    content = content.replace('\n\n', '\t')
    content = content.replace('\n', ' ')
    content = content.replace('\t', '\n')
    # content = re.sub(r'\u3000','',content)
    return content

def pdf_page_content(pdf_file, page_num):
    '''
    返回某个页面的所有layout,
    :param pdf_file: pdf文件名
    :param page_num: 页数
    :return: Generator, layout
    '''
    if page_num <= 0:
        raise ValueError('page_num must be more than zero, but the number your given is %s' %page_num)
    fp = open(pdf_file, 'rb')
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 分析器和文档相互连接
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，没有默认为空
    doc.initialize()
    # 检查文档是否可以转成TXT，如果不可以就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器，来管理共享资源
        rsrcmagr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        # 将资源管理器和设备对象聚合
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmagr, device)
        for index, page in enumerate(doc.get_pages()):
            if index != page_num - 1:
                continue
            else:
                interpreter.process_page(page)
                # 接收该页面的LTPage对象
                layout = device.get_result()
                # 这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
                # 一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
                # 想要获取文本就得获取对象的text属性
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    yield x


# pdf 按照页码读取
def pdf_pages(fp, method=None, snap_method=None, *agrs, **kwargs):
    '''
    提取pdf页码
    :param fp: 文件流 ，例如：fp = open('1.pdf','rb')
    :param method: 对每一页进行处理的方法,此函数至少有两个参数,文本和页码
    :param snap_method: 截图的任务,提取图片的方法
    :return: pdf文件的提取页
    '''
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 分析器和文档相互连接
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，没有默认为空
    doc.initialize()
    # 检查文档是否可以转成TXT，如果不可以就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器，来管理共享资源
        rsrcmagr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        # 将资源管理器和设备对象聚合
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmagr, device)
        for index, page in enumerate(doc.get_pages()):
            interpreter.process_page(page)
            # 接收该页面的LTPage对象
            layout = device.get_result()
            # 这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
            # 一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
            # 想要获取文本就得获取对象的text属性
            if snap_method:
                snap_method(index, page, layout, *agrs, **kwargs)
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    if method:
                        method(x.get_text(), index + 1, x.height, *agrs, **kwargs)


def extract_subimgs(fname, imgs_dir, n_page, type, appendix_height=0.0, *agrs, **kwargs):
    """
    提取某页面的图表
    :param fname:pdf文件名字
    :param agrs:
    :param kwargs:
    :return:
    """
    fp = open(fname, 'rb')
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 分析器和文档相互连接
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，没有默认为空
    doc.initialize()
    # 检查文档是否可以转成TXT，如果不可以就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器，来管理共享资源
        rsrcmagr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        # 将资源管理器和设备对象聚合
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmagr, device)
        my_layout = None
        for index, page in enumerate(doc.get_pages()):
            interpreter.process_page(page)
            # 接收该页面的LTPage对象
            layout = device.get_result()
            if index + 1 == int(n_page):
                my_layout = layout
                break

        current_img = os.path.join(imgs_dir, 'page_%s.png' % n_page)  # 当前图片的内容
        #print(current_img)
        save_dir = os.path.join(imgs_dir, type)  # 保存图表的文件夹
        makedir_if_not_exist(save_dir)  # 检查文件夹是否存在
        count = 0  # 计数
        history_array = []
        for sublayout in my_layout:
            if isinstance(sublayout, LTRect) or isinstance(sublayout, LTFigure):
                #print(current_img)
                #print(sublayout.height, appendix_height)
                crop_array = (int(sublayout.x0), int(sublayout.y0), int(sublayout.x1), int(sublayout.y1))  # 截取的图表位置
                if int(sublayout.width) >= 118 \
                        and (crop_array not in history_array)\
                        and int(sublayout.width) >= 169\
                        and int(sublayout.height) >= round(appendix_height) + 30\
                        and int(sublayout.width) <= 565:
                    history_array.append(crop_array)
                    if type == 'table':
                        crop_img(crop_array, current_img,save_path=os.path.join(save_dir, 'page_%s_%s.png' % (n_page, str(count))))
                    else:
                        crop_img(crop_array, current_img,appendix_height=appendix_height,
                                 save_path=os.path.join(save_dir, 'page_%s_%s.png' % (n_page, str(count))))
                    count += 1

        if count == 0: #一个图片或者表格没有找到
            shutil.copyfile(current_img, os.path.join(save_dir, 'page_%s.png' % n_page))



def pdf_title(pdf_file, page=1):
    '''
    提取pdf的标题,
    :param pdf_file: str,
        pdf文件标题
    :param page: int,
        pdf标题所在的页数，默认在第一页
    :return: str
        文献的标题
    '''
    layouts = pdf_page_content(pdf_file, page_num=page)
    tmp = ''
    for layout in layouts:
        content = layout.get_text().replace('\n','')
        if is_author(content):
            return tmp
        else:
            tmp = content
    return ''