import concurrent
import os
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path

import png


def load_images(input_dir, pattern):
    images = []
    for path in Path(input_dir).rglob(pattern):
        images.append(str(path))
    return images


def crop_image(path):
    png_reader = png.Reader(filename=path)
    output_path = path[:-4] + '_np_icon.png'
    width, height, png_pixels, metadata = png_reader.read_flat()

    del metadata['physical']
    metadata['size'] = (600, 600)

    BYTE_NUM = 4
    sliced_png_pixels = [0 for x in range(0, 600 * 600 * BYTE_NUM)]

    for row in range(0, height):
        for col in range(0, width):
            if col >= 340 and col < 940:
                if row >= 100 and row < 700:
                    sliced_png_pixels[BYTE_NUM * (row - 100) * 600 + BYTE_NUM * (col - 340)] = png_pixels[
                        BYTE_NUM * row * width + BYTE_NUM * col]
                    sliced_png_pixels[BYTE_NUM * (row - 100) * 600 + BYTE_NUM * (col - 340) + 1] = png_pixels[
                        BYTE_NUM * row * width + BYTE_NUM * col + 1]
                    sliced_png_pixels[BYTE_NUM * (row - 100) * 600 + BYTE_NUM * (col - 340) + 2] = png_pixels[
                        BYTE_NUM * row * width + BYTE_NUM * col + 2]
                    sliced_png_pixels[BYTE_NUM * (row - 100) * 600 + BYTE_NUM * (col - 340) + 3] = png_pixels[
                        BYTE_NUM * row * width + BYTE_NUM * col + 3]

    with open(output_path, 'wb') as f:
        w = png.Writer(600, 600, **metadata)
        w.write_array(f, sliced_png_pixels)

    return output_path


if __name__ == "__main__":
    all_images = load_images('/Users/shuyizhang/Documents/nft-output', '*np.png')
    executor = ThreadPoolExecutor(max_workers=8)
    batch = 8 * 10
    for i in range(0, len(all_images), batch):
        future_to_path = {executor.submit(crop_image, all_images[j]):j for j in range(i, i + batch)}

        for future in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%s failed to generate: %s' % (path, exc))
            else:
                print('%s succeeded' % (path))

