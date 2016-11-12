"""Export PNG image

Usage:
  export-image.py <image_file>

Options:
  -h --help     Show this screen.

"""
import os
from PIL import Image
from docopt import docopt

TEMPLATE_H = """#ifndef {define}
#define {define}

#include <Arduboy.h>

void draw_{image}(Arduboy &, int, int);

#endif
"""

TEMPLATE_CPP = """#include "{source}"

#include <Arduboy.h>

static const uint8_t PROGMEM {image}[{len}] = {{
    {dump}
}};

void draw_{image}(Arduboy &arduboy, int x, int y) {{
    arduboy.drawBitmap(x, y, {image}, {width}, {height}, BLACK);
}}

"""


def draw_pixel(pixel):
    red, green, blue = pixel
    gray = 0.2989 * red + 0.5870 * green + 0.1140 * blue
    is_blank = red == green == blue == 255
    return '1' if gray < 128 else '0'


def export_image(filename):
    dump = []

    basename = os.path.basename(filename)
    image_name = os.path.splitext(basename)[0]
    source_name = "{}.h".format(image_name)    
    define_name = "{}_H".format(image_name.upper())

    with Image.open(filename) as image:
        width, height = image.size
        width = width if width <= 128 else 128
        height = (height / 8) * 8
        pixels = image.load()
        height_chunks_count = height / 8

        for chunk_index in range(height_chunks_count):

            for x in range(width):
                word = 'B'

                for offset in range(8):
                    y = chunk_index * 8 + (7 - offset)
                    word += draw_pixel(pixels[x, y])

                dump.append(word)

    open(source_name, "w").write(TEMPLATE_H.format(
        define=define_name,
        image=image_name,
        len=width * height / 8,
        width=width,
        height=height,
        dump=",\n    ".join(dump)
    ))

    open(source_name.replace('.h', '.cpp'), "w").write(TEMPLATE_CPP.format(
        define=define_name,
        source=source_name,
        image=image_name,
        len=width * height / 8,
        width=width,
        height=height,
        dump=",\n    ".join(dump)
    ))


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    
    if '<image_file>' in arguments:
        export_image(arguments['<image_file>'])

