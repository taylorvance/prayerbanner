import django

from captcha.conf import settings

import random

def noise_lines(draw, image):
    size = image.size
    for i in range(4):
        draw.line([
            random.randint(0, 20),
            random.randint(int(size[1]*0.1), int(size[1]*0.7)),
            random.randint(size[0]-20, size[0]),
            random.randint(int(size[1]*0.1), int(size[1]*0.7)),
        ], fill=settings.CAPTCHA_FOREGROUND_COLOR)
    return draw

def post_sharpen(image):
    from PIL import ImageFilter
    return image.filter(ImageFilter.SHARPEN)

def post_magnify(image):
    return image.resize((
        int(image.size[0] * random.uniform(1.4, 1.6)),
        int(image.size[1] * random.uniform(1.6, 2.0))
    ))

def post_crop(image):
    return image.crop((2, 2, image.size[0]-2, int(image.size[1] * 0.8)))
