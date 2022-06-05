from PNGgraphy import *

# --------- MAIN ---------
if __name__ == '__main__':
    print(f'=== Steganography Test ===')
    message = "Thats a test abcdefghijklmnopqrstuvwxyzdflkjdfldsflsdf Test"
    go_encode = False

    if go_encode:
        file = "/home/sebastian/Develop/simon-cybersec/test/satBowl.jpg"
    else:
        file = "newCyberSec_e.png"

    with Image.open(file) as image:
        print(f'image: {image.filename}')
        print(f'format: {image.format}')
        print(f'mode: {image.mode}')
        width, height = image.size
        print(f'width: {width}, height: {height}')
        number_bytes = width * height
        print(f'total bytes #: {number_bytes}')

        if go_encode:
            encode(image, message)
        else:
            decode(image)
