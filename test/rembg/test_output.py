from rembg import remove
import os
import cv2

source = "../../source/"
out_path = "../../output/rembg/"

for file_name in os.listdir(source):
    input_path = file_name
    # a = file_name.partition('.')[0]
    # b = file_name.partition('.')[2]
    output_path = 'output_' + file_name

    print(input_path)
    print(output_path)
    print()

    input = cv2.imread(os.path.join(source, input_path))
    output = remove(input)
    cv2.imwrite(os.path.join(out_path, output_path), output)






