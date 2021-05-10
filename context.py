#!/usr/bin/env python
# coding:UTF-8

def convert_to_binary(message):
    binary_message = ''.join(format(ord(x), 'b') for x in message)
    return binary_message
