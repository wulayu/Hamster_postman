from tool import remove
import os
import time
from PIL import Image

import xlsxwriter
import sys
import importlib

importlib.reload(sys)

source = "../../source/"
out_path = "../../output/rembg/"
filename = 'time_order.xlsx'
columns_name = ['序号', '图片名称', '图片类型', '处理时间']
if not os.path.isdir(out_path):
    os.mkdir(out_path)

book = xlsxwriter.Workbook(filename)
sh = book.add_worksheet('sheet1')
sh.set_column("B:B", 93.67)
sh.set_column("D:D", 22.33)
sh.set_column("A:A", 10.33)
sh.set_column("C:C", 20)
sh.write_row('A1', columns_name)
total_time = 0

for index, file_name in enumerate(os.listdir(source)):
    time_start = time.time()

    if file_name != 'test2.png':
        continue
    input_path = file_name
    a = file_name.partition('.')[0]
    b = file_name.partition('.')[2]
    output_path = 'output_' + str(index) + '.png'

    _input = Image.open(os.path.join(source, input_path))
    _input = _input.convert(mode='RGBA')
    output = remove(_input)
    output.save(os.path.join(out_path, output_path))

    time_end = time.time()
    print(input_path)
    print(output_path)
    print(str(index + 1) + '/' + str(len(os.listdir(source))))
    print(index + 1, ' time cost', time_end - time_start, ' s', '\n')
    total_time += time_end - time_start

    data = [index + 1, a, b, str(time_end - time_start) + ' s']
    sh.write_row('A' + str(index + 2), data)

data = ['总时间：', str(total_time) + ' s']
sh.write_row('C' + str(index + 3), data)
data = ['平均时间：', str(total_time / (index + 1)) + ' s']
sh.write_row('C' + str(index + 4), data)
book.close()
