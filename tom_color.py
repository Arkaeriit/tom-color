#!/usr/bin/env python3

import png
import random

def make_png(data, filename):
    """Make a png of a table of lines"""
    img = []
    for line in data:
        row = ()
        for x in line:
            row = row + (x[0], x[1], x[2])
        img.append(row)
    with open(filename, 'wb') as f:
        w = png.Writer(len(data[0]), len(data), greyscale=False)
        w.write(f, img)

def expand_image_with_margin(data, block_size, margin_size, margin_color):
    """From a table of pixel, expand the pixel to block_size and separate them
    with a margin of margin_size."""
    full_height = (block_size + margin_size) * len(data) + margin_size
    full_width = (block_size + margin_size) * len(data[0]) + margin_size
    ret = []
    # Start with a margin
    for _ in range(margin_size):
        line = []
        for __ in range(full_width):
            line.append(margin_color)
        ret.append(line)
    for line_in in data:
        for _ in range(block_size):
            line_out = []
            # start with a margin
            for __ in range(margin_size):
                line_out.append(margin_color)
            for pixel in line_in:
                for ___ in range(block_size):
                    line_out.append(pixel)
                for ___ in range(margin_size):
                    line_out.append(margin_color)
            ret.append(line_out)
        for _ in range(margin_size):
            line_out = []
            for __ in range(full_width):
                line_out.append(margin_color)
            ret.append(line_out)
    return ret

def random_fill(height, width, palette):
    """Create a picture by randomly choosing elements from a palette."""
    ret = []
    for _ in range(height):
        line = []
        for __ in range(width):
            line.append(random.choice(palette))
        ret.append(line)
    return ret

def hex_to_rgb(hex_str):
    """Transform a string representing a hex value into a RGB list."""
    ret = [int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)]
    return ret

def hex_list_to_palette(hex_list):
    return list(map(hex_to_rgb, hex_list))

if __name__ == "__name__":
    hex_list = ["7b25bd", "a825bd", "d2bd25", "555555", "4a0792", "322c38"]
        
    _png = random_fill(10, 5, hex_list_to_palette(hex_list)) 

    make_png(expand_image_with_margin(_png, 10, 3, [255, 255, 255]), "lol.png")

