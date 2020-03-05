#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:Zgc
# datetime:2020/2/6 11:11
# software: PyCharm
import csv
from .extract_table_figure import page_handle_text
from .pdf import pdf_pages, extract_subimgs
from .pdf import read_pdf
from .utils import pdf2imgs

"""
获取pdf文本
"""
def get_content(path):
    pdf_file = path
    content = read_pdf(pdf_file)
    return content
"""
提取图表描述并写进结果当中
"""
def write_result_in_csv(csv_path,pdf_file):

    # csv_path = 'pdf_table_figure.csv'
    # fopen = open('pdf_table_figure.csv', 'w', encoding='utf-8')
    fopen = open(csv_path, 'w', encoding='utf-8')
    fopen.write("\"文件位置\",\"图表页码\",\"图表类型\",\"图表高度\",\"文字描述\"\n")
    fp = open(pdf_file, 'rb')
    pdf_pages(fp, page_handle_text, None, fopen, pdf_file)
    fopen.close()
    """
    提取图片
    """
    tf_data = None  # 图表数据 [文件位置, 图表页码, 图表类型, 文字描述]
    with open(csv_path, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        # next(rows)  # 读取首行
        tf_data = list(rows)[1:]

    for d in tf_data:
        pdf_path = d[0]
        n_page = d[1]
        type = d[2]
        appendix_height = float(d[3])
        # pdf转成图片
        pdf_img_dir = pdf2imgs(pdf_path, './tmp') # 存到主目录
        extract_subimgs(pdf_path, pdf_img_dir, n_page, type, appendix_height=appendix_height)
