from PIL import Image


def has_transparency(img):
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False


if __name__ == "__main__":
    # extract_alpha("./13.png")
    image = Image.open("../../output/rembg/output_0.png")
    # image = Image.open("../source/02-927.jpg")
    print(has_transparency(image))
