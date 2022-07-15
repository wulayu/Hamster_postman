import os
import cv2

source = "../output/rembg/"
out_path = "../output/object_detection/"
if not os.path.isdir(out_path):
    os.mkdir(out_path)


def object_detect(img):
    sp = img.shape
    print(sp)
    width = sp[1]
    height = sp[0]
    top = -1
    bottom = -1
    left = -1
    right = -1
    judge = 10  # 判决门限,门限值越大框越小
    for yh in range(height):
        count = 0
        for xw in range(width):
            color_a = img[yh][xw][3]
            if color_a != 0:
                count += 1
                if count > judge:
                    top = yh
                    break
        if top != -1:
            break
    for yh in reversed(range(height)):
        count = 0
        for xw in range(width):
            color_a = img[yh][xw][3]
            if color_a != 0:
                count += 1
                if count > judge:
                    bottom = yh
                    break
        if bottom != -1:
            break
    for xw in range(width):
        count = 0
        for yh in range(height):
            color_a = img[yh][xw][3]
            if color_a != 0:
                count += 1
                if count > judge:
                    left = xw
                    break
        if left != -1:
            break
    for xw in reversed(range(width)):
        count = 0
        for yh in range(height):
            color_a = img[yh][xw][3]
            if color_a != 0:
                count += 1
                if count > judge:
                    right = xw
                    break
        if right != -1:
            break

    # center = ((left + right) / 2, (top + bottom) / 2)
    box = [left, top, right, bottom]
    print('box =', box)
    box_color = (255, 0, 255, 255)  # 必须设置不透明度
    result = cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color=box_color, thickness=2)
    return result


if __name__ == "__main__":
    for index, file_name in enumerate(os.listdir(source)):
        # if file_name != 'output_10.png':
        #     continue
        input_path = file_name
        output_path = 'output_' + str(index) + '.png'

        _input = cv2.imread(os.path.join(source, input_path),
                            flags=cv2.IMREAD_UNCHANGED)  # "IMREAD_UNCHANGED"指定用图片的原来格式打开，以读取透明度，不加时只有rgb
        object_detect(_input)

        cv2.imshow('object', _input)
        cv2.waitKey(5000)
        cv2.imwrite(os.path.join(out_path, output_path), _input)
