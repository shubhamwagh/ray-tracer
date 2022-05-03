import numpy as np
from pathlib import Path

BASE_DIR = Path('./misc')
IMAGE_FILE_NAME = 'image.ppm'
OUTPUT_IMAGE_FILE = BASE_DIR.joinpath(IMAGE_FILE_NAME)


def main() -> None:
    # Image
    image_width = 256
    image_height = 256
    max_colour = 255

    # Render
    with open(OUTPUT_IMAGE_FILE.as_posix(), 'w') as image_file:
        image_file.write(f'P3\n{image_width} {image_height} \n{max_colour}\n')
        for j in range(image_height - 1, -1, -1):
            for i in range(0, image_width, 1):
                r = int(255.999 * i / (image_width - 1))
                g = int(255.999 * j / (image_height - 1))
                b = int(255.999 * 0.25)

                image_file.write(f'{r} {g} {b}\n')


if __name__ == "__main__":
    main()
