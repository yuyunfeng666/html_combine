# -*- coding: utf-8 -*-
# @Time    : 2020/2/7 14:28
# @Author  : Yyf
# @FileName: combine.py
# @Software: PyCharm

from pdf_to_txt import get_content, get_files
from question_answer.conclution import Qurey_answer
from docx import Document
from pdf_to_txt import write_result_in_csv
from pdf_to_txt import pdf_title
from pdf_to_txt import get_pdf_filename
import re
import sys


def combine(input_path='./stactic', output_path='res', *args, **kwargs):
    '''
    全文解读结果保存到output_path
    :param input_path: 输入的pdf文件
    :param output_path: 输出的pdf文件
    :param args: 保留参数
    :param kwargs: 保留参数
    :return:
    '''
    if re.search('.pdf', input_path, re.I):
        head_name = pdf_title(input_path)
        img_dir_name = get_pdf_filename(input_path)

        pdf_content = get_content(input_path)  # pdf提取文字，参数为pdf路径（变量）
        print(pdf_content)
        print('现在处理文档'+input_path)
        query_ans = Qurey_answer(pdf_content)  # 实例化
        document = Document()
        document.add_heading(head_name, 1)  # 参数为标题（变量）
        write_result_in_csv('pdf_to_txt/pdf_table_figure.csv', input_path)  # 第一个参数为图表信息存入的csv（固定），第二个为pdf路径（变量）
        query_ans.docx_write(document, img_dir_name,output_path, img_dir_name)  # 全文解读，第一参数为写入路径（固定），第二参数为文件名（变量）
    else:
        for file in get_files(input_path):
            combine(file,'res')


if __name__ == '__main__':
    combine("./stactic/IMpower150.pdf")

