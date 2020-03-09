import os
from logging import warning
import cv2
import fitz
from PIL import Image

def get_files(dir):
    '''
    获取当前目录下的data文件夹下的文件
    :return: data文件夹下面的pdf文件名字列表
    '''
    data_path = dir
    pdf_files = []
    for root, dirs, files in os.walk(data_path):
        pdf_files.extend([os.path.join(data_path, file) for file in files if file.endswith('.pdf')])
    return pdf_files


def crop_img(crop_array, img_path, save_path, appendix_height=0.0, zoom=3.0):
    """
    裁剪img，获取img某个区域的图片对象并保存
    :param crop_array: 裁剪的区域(左，上，右，下）
    :param img_path: 图片的路径
    :param save_path: 保存图片的路径
    :param zoom: 图片缩放的大小
    :return:
    """
    if len(crop_array) != 4:
        raise ValueError('The length of crop_array is 4, rather %s' % len(crop_array))
    crop_array = list(crop_array)
    img = Image.open(img_path)
    zoom_height = img.size[1]  # 缩放后的高度
    height = zoom_height / zoom  # 转换为原本的高度
    # pdf中的坐标上下的位置需要转换
    tmp = height - crop_array[1]  # 上面的坐标
    crop_array[1] = height - crop_array[3]  # 上面的坐标
    crop_array[3] = tmp + appendix_height
    crop_array = tuple(map(lambda x: x * zoom, crop_array))
    try:
        cropped = img.crop(crop_array)  # (left, upper, right, lower)
    except:
        warning('%s 截取失败，有可能截取超出界限请检查%s' % (img_path, str(crop_array)))
    cropped.save(save_path)

def makedir_if_not_exist(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def pdf2imgs(pdf_path, imgs_dir, zoom=3.0):
    """
    PDF文件转成图片，
    :param pdf_path: pdf文件的路径
    :param imgs_dir: img文件存储的文件夹
    :param zoom_x: x缩放的倍数
    :param zoom_y: y缩放的倍数
    :return:pdf图片的文件夹
    """
    doc = fitz.open(pdf_path)  # pdf路径
    pdf_name = get_pdf_filename(pdf_path)
    if not os.path.isfile(imgs_dir):
        makedir_if_not_exist(imgs_dir)
    else:
        raise ValueError('%s must be a dictionary rather a file.' % imgs_dir)
    pdf_img_dir = os.path.join(imgs_dir, pdf_name)
    if os.path.exists(pdf_img_dir):
        #print('文件已经存在！')
        return pdf_img_dir
    else:
        os.mkdir(pdf_img_dir)

    for pg in range(doc.pageCount):
        page = doc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
        zoom_x = zoom_y = zoom
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        img_tmp = os.path.join(pdf_img_dir, 'page_%s.png' % str(pg + 1))
        pm.writePNG(img_tmp)  # 最终存储路径
        #print('提取图片保存成功：', img_tmp)
    return pdf_img_dir

def _judge_words(content):
    '''

    :param content:
    :return:
    '''
    if len(content.lstrip().rstrip().split(' ')) > 6:
        return False
    else:
        return True

def is_author(content):
    """
    判断这句话里面有多少个作者
    :param content: 文本输入进去
    :return: bool, 是否有多个人名
    """
    anthors = content.split(',')
    results = map(_judge_words, anthors)
    flag = True
    for r in results:
        if not r:
            flag = False
    if len(anthors) > 2 and flag:
        return True
    else:
        return False

def get_pdf_filename(pdf_path):
    return os.path.splitext(os.path.split(pdf_path)[-1])[0]

def get_crop_array(img_file):
    pass