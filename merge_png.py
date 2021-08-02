import bpy
import sys
import os
import png
import array
import json
import copy
import random

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')

def alphablend(p_dst, p_src, w, h):
    BYTE_NUM = 4
    p_out = p_dst
    row = 0
    col = 0
    for row in range(0, h):
        for col in range(0, w):
            dst_a = p_dst[BYTE_NUM * row * w + BYTE_NUM * col + 3] / 255
            src_a = p_src[BYTE_NUM * row * w + BYTE_NUM * col + 3] / 255
            out_a = src_a + (dst_a * (1 - src_a))

            dst_r = p_dst[BYTE_NUM * row * w + BYTE_NUM * col]
            src_r = p_src[BYTE_NUM * row * w + BYTE_NUM * col]

            dst_g = p_dst[BYTE_NUM * row * w + BYTE_NUM * col + 1]
            src_g = p_src[BYTE_NUM * row * w + BYTE_NUM * col + 1]

            dst_b = p_dst[BYTE_NUM * row * w + BYTE_NUM * col + 2]
            src_b = p_src[BYTE_NUM * row * w + BYTE_NUM * col + 2]

            out_r = (src_r * src_a + dst_r * dst_a * ( 1 - src_a )) / out_a
            out_g = (src_g * src_a + dst_g * dst_a * ( 1 - src_a )) / out_a
            out_b = (src_b * src_a + dst_b * dst_a * ( 1 - src_a )) / out_a

            #print(int(out_r))
            #print(int(out_g))
            #print(int(out_b))
            p_out[BYTE_NUM * row * w + BYTE_NUM * col] = int(out_r)
            p_out[BYTE_NUM * row * w + BYTE_NUM * col + 1] = int(out_g)
            p_out[BYTE_NUM * row * w + BYTE_NUM * col + 2] = int(out_b)
            p_out[BYTE_NUM * row * w + BYTE_NUM * col + 3] = int(out_a * 255)

            col = col + 1

        row = row + 1

    return p_out

def get_all_png(path):
    pngs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return pngs

def merge():
    output_path = os.path.join(data_dir, "output", "lianpu")
    input_path = os.path.join(data_dir, "input", "lianpu")
    input_base_path = os.path.join(input_path, "base")
    input_eyebrow_path = os.path.join(input_path, "eyebrow")
    input_eye_path = os.path.join(input_path, "eye")
    input_mouth_path = os.path.join(input_path, "mouth")
    input_random_path = os.path.join(input_path, "random_use")
    input_random2_path = os.path.join(input_path, "random_use_2")

    #width = 0
    #height = 0
    #metadata = None

    out_name_prefix = "composite"

    base_pngs = get_all_png(input_base_path)
    eyebrow_pngs = get_all_png(input_eyebrow_path)
    eye_pngs = get_all_png(input_eye_path)
    mouth_pngs = get_all_png(input_mouth_path)
    random_pngs = get_all_png(input_random_path)
    random_count = len(random_pngs)
    random_usage = {}

    random2_pngs = get_all_png(input_random2_path)
    random2_count = len(random2_pngs)
    random2_usage = {}

    for base_png in base_pngs:
        base_id = base_png.split('.')[0].split('_')[1]
        base_png_path = os.path.join(input_base_path, base_png)
        base_png_reader = png.Reader(filename=base_png_path)
        width, height, base_png_pixels, metadata = base_png_reader.read_flat()

        for eyebrow_png in eyebrow_pngs:
            eyebrow_id = eyebrow_png.split('.')[0].split('_')[1]
            eyebrow_png_path = os.path.join(input_eyebrow_path, eyebrow_png)
            eyebrow_png_reader = png.Reader(filename=eyebrow_png_path)
            _, _, eyebrow_png_pixels, _ = eyebrow_png_reader.read_flat()

            for eye_png in eye_pngs:
                eye_id = eye_png.split('.')[0].split('_')[1]
                eye_png_path = os.path.join(input_eye_path, eye_png)
                eye_png_reader = png.Reader(filename=eye_png_path)
                _, _, eye_png_pixels, _ = eye_png_reader.read_flat()

                for mouth_png in mouth_pngs:
                    mouth_id = mouth_png.split('.')[0].split('_')[1]
                    mouth_png_path = os.path.join(input_mouth_path, mouth_png)
                    mouth_png_reader = png.Reader(filename=mouth_png_path)
                    _, _, mouth_png_pixels, _ = mouth_png_reader.read_flat()

                    composite_pixels = copy.deepcopy(base_png_pixels)
                    composite_pixels = alphablend(composite_pixels, eyebrow_png_pixels, width, height)
                    composite_pixels = alphablend(composite_pixels, eye_png_pixels, width, height)
                    composite_pixels = alphablend(composite_pixels, mouth_png_pixels, width, height)

                    random_idx = random.randint(0, random_count-1)
                    if not random_idx in random_usage:
                        random_usage[random_idx] = 0
                    random_png = random_pngs[random_idx]
                    random_usage_limit = int(random_png.split('=')[0])

                    try_count = 0
                    while(random_usage[random_idx] >= random_usage_limit):
                        random_idx = random.randint(0, random_count-1)
                        if not random_idx in random_usage:
                            random_usage[random_idx] = 0
                        random_png = random_pngs[random_idx]
                        random_usage_limit = int(random_png.split('=')[0])
                        try_count = try_count + 1
                        if try_count >= 10000:
                            print("!!!!!!!!!!!!!!!!!!")
                            break
                    
                    random_usage[random_idx] = random_usage[random_idx] + 1
                    random_id = random_png.split('.')[0].split('_')[1]
                    random_png_path = os.path.join(input_random_path, random_png)
                    random_png_reader = png.Reader(filename=random_png_path)
                    _, _, random_png_pixels, _ = random_png_reader.read_flat()

                    composite_pixels = alphablend(composite_pixels, random_png_pixels, width, height)


                    random2_idx = random.randint(0, random2_count-1)
                    if not random2_idx in random2_usage:
                        random2_usage[random2_idx] = 0
                    random2_png = random2_pngs[random2_idx]
                    random2_usage_limit = int(random2_png.split('=')[0])

                    try_count = 0
                    while(random2_usage[random2_idx] >= random2_usage_limit):
                        random2_idx = random.randint(0, random2_count-1)
                        if not random2_idx in random2_usage:
                            random2_usage[random2_idx] = 0
                        random2_png = random2_pngs[random2_idx]
                        random2_usage_limit = int(random2_png.split('=')[0])
                        try_count = try_count + 1
                        if try_count >= 10000:
                            print("!!!!!!!!!!!!!!!!!!")
                            break
                    
                    random2_usage[random2_idx] = random2_usage[random2_idx] + 1
                    random2_id = random2_png.split('.')[0].split('_')[1]
                    random2_png_path = os.path.join(input_random2_path, random2_png)
                    random2_png_reader = png.Reader(filename=random2_png_path)
                    _, _, random2_png_pixels, _ = random2_png_reader.read_flat()

                    composite_pixels = alphablend(composite_pixels, random2_png_pixels, width, height)


                    png_out = os.path.join(output_path, out_name_prefix + "_" + base_id + "_" + eyebrow_id + "_" + eye_id + "_" + mouth_id + "_" + random_id + "_" + random2_id + ".png")
                    f = open(png_out, 'wb')
                    w = png.Writer(width, height, **metadata)
                    w.write_array(f, composite_pixels)
                    f.close()

if __name__ == "__main__":
    merge()