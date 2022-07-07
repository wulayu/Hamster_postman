from rembg import remove
import os
import cv2

source = "../../source/"
out_path = "../../output/rembg/"
if not os.path.isdir(out_path):
    os.mkdir(out_path)

for index, file_name in enumerate(os.listdir(source)):
    input_path = file_name
    # a = file_name.partition('.')[0]
    # b = file_name.partition('.')[2]
    output_path = 'output_' + file_name

    print(input_path)
    print(output_path)
    print(str(index + 1) + '/' + str(len(os.listdir(source))) + '\n')

    _input = cv2.imread(os.path.join(source, input_path))
    output = remove(_input)
    cv2.imwrite(os.path.join(out_path, output_path), output)
