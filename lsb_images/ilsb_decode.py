#!/usr/bin/env python3

# Script for message retrieval
# Last Significant Bit steganography for RGB images
# by Vz 2018

from PIL import Image
import sys

bits_in_byte = 8

def decode(container, width, height, message_len, rgb_channel):
    result_bits = []
    channels = dict()
    ms_len_counter = 0
    for x in range(0, width):
        for y in range(0, height):
            if ms_len_counter == message_len * bits_in_byte:
                return result_bits
            ms_len_counter += 1
            channels['R'], channels['G'], channels['B'] = container.getpixel((x, y))
            result_bits.append(channels[rgb_channel] & 1)

container_filename = input("message container: ")
try:
    container_image = Image.open(container_filename)
except:
    print("error during opening the container")
    sys.exit(1)
message_len = int(input("length of message: "))
width, height = container_image.size
rgb_ch = input("choose rgb channel (R/G/B): ")
if rgb_ch not in ('R', 'G', 'B'):
    print("wrong channel value")
    sys.exit(1)

message_bits = decode(container_image, width, height, message_len, rgb_ch)
message_string = []
for byte in range(0, message_len):
  ascii_code = 0
  for bit in range(0,8):
      ascii_code = ascii_code * 2 + message_bits[byte * bits_in_byte + bit]
  message_string.append(chr(ascii_code))

print("OK:", "".join(message_string))
