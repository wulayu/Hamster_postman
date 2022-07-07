from rembg import remove
import os
import cv2
import time

source = "../../source/"
out_path = "../../output/rembg/"
if not os.path.isdir(out_path):
    os.mkdir(out_path)

time_start = time.time()

for index, file_name in enumerate(os.listdir(source)):
    if file_name != '02-927.jpg':
        continue
    input_path = file_name
    # a = file_name.partition('.')[0]
    # b = file_name.partition('.')[2]
    output_path = 'output_' + file_name

    print(input_path)
    print(output_path)
    print(str(index + 1) + '/' + str(len(os.listdir(source))) + '\n')

    _input = cv2.imread(os.path.join(source, input_path))
    output = remove(_input, alpha_matting_background_threshold=100)
    cv2.imwrite(os.path.join(out_path, output_path), output)

time_end = time.time()
print('time cost', time_end - time_start, 's')
