from pathlib import Path

import pygame


IMAGE_DIR = Path(__file__).parent / "images"

_image_cache = {}


def load_image(filename, size=None, alpha=True):
    cache_key = (filename, size, alpha)

    if cache_key in _image_cache:
        return _image_cache[cache_key]

    image = pygame.image.load(IMAGE_DIR / filename)
    image = image.convert_alpha() if alpha else image.convert()

    if size is not None:
        image = pygame.transform.scale(image, size)

    _image_cache[cache_key] = image
    return image
