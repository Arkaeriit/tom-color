#!/usr/bin/env python3

import png
import random

def make_png(data, filename):
    """Make a png of a table of lines"""
    img = []
    for line in data:
        row = []
        for x in line:
            for i in range(3):
                row.append(x[i])
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

def random_fill(height, width, palette, palette_max_count):
    """Create a picture by randomly choosing elements from a palette."""
    ret = []
    color_count_map = {str(palette[i]): {"max": palette_max_count[i], "current": 0} for i in range(len(palette_max_count))}
    for _ in range(height):
        line = []
        for __ in range(width):
            color = random.choice(palette) 
            while color_count_map[str(color)]["current"] >= color_count_map[str(color)]["max"]:
                color = random.choice(palette) 
            color_count_map[str(color)]["current"] += 1
            line.append(color)
        ret.append(line)
    return ret

def hex_to_rgb(hex_str):
    """Transform a string representing a hex value into a RGB list."""
    ret = [int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)]
    return ret

def hex_list_to_palette(hex_list):
    return list(map(hex_to_rgb, hex_list))

if __name__ == "__main__":
    hex_list = ["7b25bd", "a825bd", "d2bd25", "555555", "4a0792", "322c38"]
    palette_max_count = [50 for i in range(len(hex_list))]
        
    _png = random_fill(10, 5, hex_list_to_palette(hex_list), palette_max_count)

    make_png(expand_image_with_margin(_png, 100, 30, [255, 255, 255]), "lol.png")

