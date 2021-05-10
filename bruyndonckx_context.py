#!/usr/bin/env python
# coding:UTF-8
from bruyndonckx_pixel import BruyndonckxPixel
import context
import bruyndonckx_math
import math

DEFAULT_CHANNEL = 0

class SteganographyException(Exception):
    pass

def encode_blocks(image, image_blocks, binary_message, level):
    for index in range(0, len(binary_message), 1):
        delta = 0
        letter = binary_message[index]
        image_block = image_blocks[index]
        count_a1 = bruyndonckx_math.countA1(image_block)
        count_a2 = bruyndonckx_math.countA2(image_block)
        count_b1 = bruyndonckx_math.countB1(image_block)
        count_b2 = bruyndonckx_math.countB2(image_block)
        mean_a1 = bruyndonckx_math.meanA1(image_block)
        mean_a2 = bruyndonckx_math.meanA2(image_block)
        mean_b1 = bruyndonckx_math.meanB1(image_block)
        mean_b2 = bruyndonckx_math.meanB2(image_block)
        mean_ab1 = bruyndonckx_math.meanAB1(image_block)
        mean_ab2 = bruyndonckx_math.meanAB2(image_block)

        if letter == '0':
            upd_mean_a1 = mean_ab1 - (level * count_b1) / (count_a1 + count_b1)
            upd_mean_b1 = upd_mean_a1 + level
            upd_mean_a2 = mean_ab2 - (level * count_b2) / (count_a2 + count_b2)
            upd_mean_b2 = upd_mean_a2 + level
        else:
            upd_mean_a1 = mean_ab1 + (level * count_b1) / (count_a1 + count_b1)
            upd_mean_b1 = upd_mean_a1 - level
            upd_mean_a2 = mean_ab2 + (level * count_b2) / (count_a2 + count_b2)
            upd_mean_b2 = upd_mean_a2 - level

        for br_pixel in image_block:
            if (br_pixel.brightness_marker == 1) & (br_pixel.mask_marker == 'A'):
                delta = upd_mean_a1 - mean_a1
            elif (br_pixel.brightness_marker == 2) & (br_pixel.mask_marker == 'A'): 
                delta = upd_mean_a2 - mean_a2
            elif (br_pixel.brightness_marker == 1) & (br_pixel.mask_marker == 'B'): 
                delta = upd_mean_b1 - mean_b1
            elif (br_pixel.brightness_marker == 2) & (br_pixel.mask_marker == 'B'): 
                delta = upd_mean_b2 - mean_b2
            else:
                raise SteganographyException("Unknown pixel type")

            image[br_pixel.x, br_pixel.y][DEFAULT_CHANNEL] = image[br_pixel.x, br_pixel.y][DEFAULT_CHANNEL] + (delta)
        
    return image
        
def decode_blocks(image_blocks):
    decoded_message = ''
    for image_block in image_blocks:

        count_a1 = bruyndonckx_math.countA1(image_block)
        count_a2 = bruyndonckx_math.countA2(image_block)
        count_b1 = bruyndonckx_math.countB1(image_block)
        count_b2 = bruyndonckx_math.countB2(image_block)
        mean_a1 = bruyndonckx_math.meanA1(image_block)
        mean_a2 = bruyndonckx_math.meanA2(image_block)
        mean_b1 = bruyndonckx_math.meanB1(image_block)
        mean_b2 = bruyndonckx_math.meanB2(image_block)
        mean_ab1 = bruyndonckx_math.meanAB1(image_block)
        mean_ab2 = bruyndonckx_math.meanAB2(image_block)

        diff_1 = mean_a1 - mean_b1
        diff_2 = mean_a2 - mean_b2

        if (diff_1 * diff_2 > 0):
            decoded_message += '1' if diff_1 > 0 else '0'
        elif (diff_1 * diff_2 < 0):
            diff = (count_a1 + count_b1) * diff_1 + (count_a2 + count_b2) * diff_2
            decoded_message += '1' if diff > 0 else '0'
        else:
            diff = diff_1 if diff_1 > diff_2 else diff_2
            decoded_message += '1' if diff > 0 else '0'
    return decoded_message

# Для каждого пикселя блока 8 на 8, создается экземпляр класса BruyndonckxPixel. Значения brightness_marker 
# и mask_marker определяются по brightness_threshold и маске. Все пиксели разделены на 4 типа:
# A1 - пиксель имеет значение А в маске, и яркость ниже пороговой.
# A2 - пиксель имеет значение А в маске, и яркость выше пороговой.
# B1 - пиксель имеет значение B в маске, и яркость ниже пороговой.
# B2 - пиксель имеет значение B в маске, и яркость выше пороговой.
def create_bruyndonckx_pixels_blocks(image, tile_size = 8):
    blocks = []
    height, width, nbchannels = image.shape
    
    for h in range(0, height - tile_size, tile_size):
        for w in range(0, width - tile_size, tile_size):
            sub_block = []
            sorted_brightness_block = sort_brightness_block(image, h, w)
            brightness_threshold = count_brightness_threshold(sorted_brightness_block)
            for tmp_h in range(h, h + 8, 1):
                for tmp_w in range(w, w + 8, 1):
                    if (((tmp_w < w + 4) & (tmp_h < h + 4)) | ((tmp_w >= w + 4) & (tmp_h >= h + 4))):
                        if (((tmp_h - h) * 8) + (tmp_w - w) <= brightness_threshold):
                            sub_block.append(BruyndonckxPixel(tmp_h, tmp_w, image[tmp_h, tmp_w][DEFAULT_CHANNEL], 1, 'A'))
                        else:
                            sub_block.append(BruyndonckxPixel(tmp_h, tmp_w, image[tmp_h, tmp_w][DEFAULT_CHANNEL], 2, 'A'))
                    else:
                        if (((tmp_h - h) * 8)  + (tmp_w - w) <= brightness_threshold):
                            sub_block.append(BruyndonckxPixel(tmp_h, tmp_w, image[tmp_h, tmp_w][DEFAULT_CHANNEL], 1, 'B'))
                        else:
                            sub_block.append(BruyndonckxPixel(tmp_h, tmp_w, image[tmp_h, tmp_w][DEFAULT_CHANNEL], 2, 'B'))
            blocks.append(sub_block)
    return blocks

def sort_brightness_block(image, h, w):
    block = []
    for tmp_h in range(h, h + 8, 1):
        for tmp_w in range(w, w + 8, 1):
            block.append(image[tmp_h, tmp_w][DEFAULT_CHANNEL])
    return sorted(block)


def count_brightness_threshold(brightness_block):
    # Длина переданного массива пикселей (известно 64)
    # Решено взять расмотрение среднего участка яркостей
    # 25% - 50% - 25%
    # Поэтому нижнюю границу поиска производной
    # мы берем 64*0.25 = 16, верхнюю 64*0.75 = 48 
    # lenmin = 15
    # lenmax = 47
    # # Параметр для примерного расчета производной
    # h = 1
    # max_val = 0
    # max_index = -1 
    # while lenmin < lenmax:
    #     tmp = (brightness_block[lenmin + h] - brightness_block[lenmin - h]) / (2 * h)
    #     if (tmp >= max_val):
    #         max_val = tmp
    #         max_index = lenmin
    #     lenmin += 1
    return 32

def validate_message_len(height, width, binary_message):
    if len(binary_message) > math.floor(height / 8) * math.floor(width / 8):
        raise SteganographyException("Size of message more then 8*8 blocks in image")
    return True

def countA1(block):
    count = 0
    for br_pixel in block:
        if (br_pixel.brightness_marker == 1) & (br_pixel.mask_marker == 'A'):
            count += 1
    return count


def countA2(block):
    count = 0
    for br_pixel in block:
        if (br_pixel.brightness_marker == 2) & (br_pixel.mask_marker == 'A'):
            count += 1
    return count

def countB1(block):
    count = 0
    for br_pixel in block:
        if (br_pixel.brightness_marker == 1) & (br_pixel.mask_marker == 'B'):
            count += 1
    return count

def countB2(block):
    count = 0
    for br_pixel in block:
        if (br_pixel.brightness_marker == 2) & (br_pixel.mask_marker == 'B'):
            count += 1
    return count

def meanA1(block):
    sum_val = 0
    count = 0
    for br_pixel in block:
        if (br_pixel.brightness_marker == 1) & (br_pixel.mask_marker == 'A'):
            sum_val += br_pixel.value
            count += 1
    return sum_val / count if count != 0 else 0

def meanA2(block):
    sum_val = 0
    count = 0
    for br_pixel in block:
        if (br_pixel.brightness_marker == 2) & (br_pixel.mask_marker == 'A'):
            sum_val += br_pixel.value
            count += 1
    return sum_val / count if count != 0 else 0

def meanB1(block):
    sum_val = 0
    count = 0
    for br_pixel in block:
        if (br_pixel.brightness_marker == 1) & (br_pixel.mask_marker == 'B'):
            sum_val += br_pixel.value
            count += 1
    return sum_val / count if count != 0 else 0

def meanB2(block):
    sum_val = 0
    count = 0
    for br_pixel in block:
        if (br_pixel.brightness_marker == 2) & (br_pixel.mask_marker == 'B'):
            sum_val += br_pixel.value
            count += 1
    return sum_val / count if count != 0 else 0

def meanAB1(block):
    sum_val = 0
    count = 0
    for br_pixel in block:
        if br_pixel.brightness_marker == 1:
            sum_val += br_pixel.value
            count += 1
    return sum_val / count if count != 0 else 0

def meanAB2(block):
    sum_val = 0
    count = 0
    for br_pixel in block:
        if br_pixel.brightness_marker == 2:
            sum_val += br_pixel.value
            count += 1
    return sum_val / count if count != 0 else 0