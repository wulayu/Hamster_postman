from rembg import remove
import os
import time
from PIL import Image

source = "../../source/"
out_path = "../../output/rembg/"
if not os.path.isdir(out_path):
    os.mkdir(out_path)

time_start = time.time()

for index, file_name in enumerate(os.listdir(source)):
    # if file_name != '02-927.jpg':
    #     continue
    input_path = file_name
    # a = file_name.partition('.')[0]
    # b = file_name.partition('.')[2]
    output_path = 'output_' + str(index) + '.png'

    print(input_path)
    print(output_path)
    print(str(index + 1) + '/' + str(len(os.listdir(source))) + '\n')

    _input = Image.open(os.path.join(source, input_path))
    _input = _input.convert(mode='RGBA')
    output = remove(_input)
    output.save(os.path.join(out_path, output_path))

time_end = time.time()
print('time cost', time_end - time_start, 's')
