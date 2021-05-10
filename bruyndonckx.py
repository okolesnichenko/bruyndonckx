#!/usr/bin/env python
# coding:UTF-8
"""LSBSteg.py

Usage:
  Bruyndonckx.py encode -i <input> -o <output> -f <file>
  Bruyndonckx.py decode -i <input>

Options:
  -h, --help                Show this help
  --version                 Show the version
  -f,--file=<file>          File to hide
  -i,--in=<input>           Input image (carrier)
  -o,--out=<output>         Output image (or extracted file)
"""

import cv2
import docopt
import context
import image_slicer
import bruyndonckx_context
import numpy as np
from skimage.util import random_noise


def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err

def max_d(imageA, imageB):
    err = np.sum(np.abs(np.subtract(imageA, imageB, dtype=np.float64))) / imageA.shape[0]

    return err


def minkowski(imageA, imageB, p):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** p)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err ** (1 / p)


class Bruyndonckx():
    def __init__(self, file_path):
        self.file_path = file_path
        self.image = cv2.imread(file_path)
        self.height, self.width, self.nbchannels = self.image.shape
        self.size = self.width * self.height
        self.deep_level = 10 # Constant for Bruyndonckx encodeing

    def encode(self, message):
        binary_message = context.convert_to_binary(message)
        print(binary_message)
        bruyndonckx_context.validate_message_len(self.height, self.width, binary_message)
        image_blocks = bruyndonckx_context.create_bruyndonckx_pixels_blocks(self.image)
        changed_image = bruyndonckx_context.encode_blocks(self.image, image_blocks, binary_message, self.deep_level)
        return changed_image


    def decode(self):
        image_blocks = bruyndonckx_context.create_bruyndonckx_pixels_blocks(self.image)
        message = bruyndonckx_context.decode_blocks(image_blocks)
        return message


def main():
    args = docopt.docopt(__doc__, version="0.2")
    in_f = args["--in"]
    out_f = args["--out"]
    steg = Bruyndonckx(in_f)
    lossy_formats = ["jpeg", "jpg"]

    if args['encode']:
        # Handling lossy format
        out_f, out_ext = out_f.split(".")
        if out_ext in lossy_formats:
            out_f = out_f + ".png"
            print("Output file changed to ", out_f)

        message = open(args["--file"], "r").read()
        res = steg.encode(message)
        cv2.imwrite(out_f, res)

    elif args["decode"]:
        decoded_message = steg.decode()
        orig_text = open('text.txt', "r").read()
        # Я долго разбирался как 101001001010 привести в string, но сотавлю сравнение байтов.
        print('Encoded:', context.convert_to_binary(orig_text))
        print("Decoded:", decoded_message[0:len(context.convert_to_binary(orig_text))])

    # # Вычисление метрик
    # image1 = cv2.imread('forest.png')
    # image2 = cv2.imread('any2.png')
    # mse_ressult = mse(image1, image2)
    # print('MSE: ' + str(mse_ressult))
    # max_d_result = max_d(image1, image2)
    # print('MAXD: ' + str(max_d_result))
    # minkowski_result = minkowski(image1, image2, 4)
    # print('Minkowski: ' + str(minkowski_result))

    # # Проверка устойчивости к аддитивному шуму
    # img_after_gaus_gauss = random_noise(image2, mode='gaussian', seed=None, clip=True)
    # steg = LSBSteg(img_after_gaus_gauss)
    # raw = steg.decode_binary()
    # with open('text_with_noise.txt', "wb") as f:
    #     f.write(raw)



if __name__ == "__main__":
    main()
