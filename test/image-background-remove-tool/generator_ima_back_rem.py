import importlib
import os
import sys
import time
from decimal import Decimal

import PIL.Image
import xlsxwriter
from carvekit.api.interface import Interface
from carvekit.ml.wrap.fba_matting import FBAMatting
from carvekit.ml.wrap.u2net import U2NET
from carvekit.pipelines.postprocessing import MattingMethod
from carvekit.pipelines.preprocessing import PreprocessingStub
from carvekit.trimap.generator import TrimapGenerator

importlib.reload(sys)


source = "../../source/"
out_path = "../../output/image-background-remove-tool/"
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

    # if file_name != '02-927.jpg':
    #     continue
    input_path = file_name
    x = input_path.rsplit(".", 1)
    output_path = 'output_' + str(index) + '.png'

    u2net = U2NET(device='cpu', batch_size=1)
    fba = FBAMatting(device='cpu', input_tensor_size=2048, batch_size=1)
    tri_map = TrimapGenerator()
    preprocessing = PreprocessingStub()
    postprocessing = MattingMethod(matting_module=fba, trimap_generator=tri_map, device='cpu')
    interface = Interface(pre_pipe=preprocessing, post_pipe=postprocessing, seg_pipe=u2net)

    image = PIL.Image.open(os.path.join(source, input_path))
    image = image.convert_url(mode='RGBA')
    cat_wo_bg = interface([image])[0]
    cat_wo_bg.save(os.path.join(out_path, output_path), format='png')

    time_end = time.time()
    print(input_path)
    print(output_path)
    print(str(index + 1) + '/' + str(len(os.listdir(source))))
    print(index + 1, ' time cost', Decimal(time_end - time_start).quantize(Decimal("0.00")), ' s', '\n')
    total_time += time_end - time_start

    data = [index + 1, x[0], x[-1], str(Decimal(time_end - time_start).quantize(Decimal("0.00"))) + ' s']
    sh.write_row('A' + str(index + 2), data)

data = ['总时间：', str(Decimal(total_time).quantize(Decimal("0.00"))) + ' s']
sh.write_row('C' + str(len(os.listdir(source)) + 2), data)
data = ['平均时间：', str(Decimal(total_time / len(os.listdir(source))).quantize(Decimal("0.00"))) + ' s']
sh.write_row('C' + str(len(os.listdir(source)) + 3), data)
book.close()
