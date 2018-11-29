#!/usr/bin/env python3

# Script for message insertion
# Last Significant Bit steganography for RGB images
# by Vz, 2018

from PIL import Image
import sys

bits_in_byte = 8
last_bit_zero_mask = 254
last_bit_one_mask = 1

input_filenames = []
if len(sys.argv) > 1:
    input_filenames = sys.argv[1:]
else:
    input_filenames.append(input("original container file name: "))

for orig_filename in input_filenames:

    try:
        orig_image = Image.open(orig_filename)
    except:
        print("Error: error during opening the container", "ERR: " + orig_filename, sep = '\n')
        continue
    width, height = orig_image.size
    new_filename = input("generated image file name: ")
    if new_filename.find(".") == -1:
        new_filename = new_filename + ".png"
    rgb_ch = input("choose rgb channel (R/G/B): ")
    while rgb_ch not in ('R', 'G', 'B'):
        print("Error: wrong channel value")
        rgb_ch = input("choose rgb channel (R/G/B): ")
    message = input("message: ")

    try:
        message.encode("ascii")
    except UnicodeEncodeError:
        print("Error: message is not in ascii", "ERR: " + orig_filename, sep = '\n')
        continue

    if (len(message) * bits_in_byte > width * height):
        print("Error: message is too big for this container", "ERR: " + orig_filename, sep = '\n')
        continue

    new_image = Image.new("RGB", (width, height))

    ascii_codes = [ord(symbol) for symbol in list(message)]
    message_bits = []

    for code in ascii_codes:
        bit_list = [int(bit) for bit in bin(code)[2:]]
        bit_list = [0] * (bits_in_byte - len(bit_list)) + bit_list
        message_bits += bit_list

    mes_bits_counter = 0
    channels = dict()
    for x in range(width):
        for y in range(height):
            channels['R'], channels['G'], channels['B'] = orig_image.getpixel((x, y))
            if mes_bits_counter < len(message_bits):
                if message_bits[mes_bits_counter] == 0:
                    channels[rgb_ch] &= last_bit_zero_mask
                else:
                    channels[rgb_ch] |= last_bit_one_mask
            new_image.putpixel((x,y), (channels['R'], channels['G'], channels['B']))
            mes_bits_counter += 1

    try:
        new_image.save(new_filename)	
    except:
        print("Error: error during saving file", "ERR: " + orig_filename, sep = '\n')
        continue

    print("OK:", new_filename)
