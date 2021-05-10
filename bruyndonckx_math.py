#!/usr/bin/env python
# coding:UTF-8

import math

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