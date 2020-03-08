#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time    : 2020/1/6 11:10
@Author  : BioKnowZG
@File    : extract_table_figure.py
@Software: PyCharm
"""

import re

def page_handle_text(content, n_page, height, *args, **kwargs):
    '''
    提取每一页的表格或者图片的，接口方法在pdf_pages方法中调用
    :param content:pdf的文字和地方变量
    :param n_page:页码数
    :param args:
    :param kwargs:
    :return:
    '''
    # Figure 匹配
    rc = re.compile(r'^(Figure|Fig|FIGURE)')
    # rc = re.compile('Figure\s*\d+\s*:\s*[\s\S]*|Figure\s*\d+\s*.\s*[\s\S]*|Fig\s*\d+\s*:\s*[\s\S]*|Fig\s*\d+\s*:\s*[\s\S]*')
    fig_tabel = rc.findall(content.lstrip())
    if fig_tabel:
        result = content
        try:
            rlist = result.split('\n')
            result = rlist[0] + '\n' + ' '.join(rlist[1:])
        except:
            pass
        write_csv(args[0], args[1], n_page, 'figure', height ,result)
    # Table 匹配
    rc = re.compile('^(Table|Tab|TABLE)')
    # rc = re.compile('Table\s*\d+\s*:\s*|Table\s*\d+\s*.\s*')
    fig_tabel = rc.findall(content)
    if fig_tabel:
        result = content
        try:
            rlist = result.split('\n')
            result = rlist[0] + '\n' + ' '.join(rlist[1:])
        except:
            pass
        write_csv(args[0], args[1], n_page, 'table', height, result)


def write_csv(f, file, n_page, type, height, result):
    '''
    把图表信息保存到表格当中
    :param f: f是open()函数的事例
    :param file: pdf的文件名
    :param n_page: 多少页
    :param type: 图片还是表格
    :param height: 表格描述的高度
    :param result: 表格描述
    :return:
    '''
    f.write('\"' + file + '\",' + '\"' + str(n_page) + '\",' + '\"' + type + '\",' + '\"' + str(height) + '\",' + '\"' + result + '\",\n')


if __name__ == '__main__':
    raise RuntimeError(r'You can\'t import this as a model!')