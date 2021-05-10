#!/usr/bin/env python
# coding:UTF-8

class BruyndonckxPixel():
    def __init__(self, x, y, value, brightness_marker, mask_marker):
        self.x = x # Coordinates of image
        self.y = y # Coordinates of image
        self.value = value # Coordinates of image
        self.brightness_marker = brightness_marker # 1 or 2
        self.mask_marker = mask_marker # A or B


        # Current mask
        # A A A A B B B B
        # A A A A B B B B
        # A A A A B B B B
        # A A A A B B B B
        # B B B B A A A A
        # B B B B A A A A
        # B B B B A A A A
        # B B B B A A A A
