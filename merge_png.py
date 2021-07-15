import bpy
import sys
import os
import png
import array
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')

class ConfigNotFoundError(Exception):
    pass

def get_resource_data(resource_data, data_id, data_category=None):
    res_founded = None
    for r in resource_data:
        r_id = round(r["ID"])
        if r_id == int(data_id):
            res_founded = r
            break

    if res_founded == None:
        raise ConfigNotFoundError("resource data not found ! please check resource.xls or run generate_config script! ID : " + str(data_id))

    return res_founded

def merge(argv):
    output_path = os.path.join(data_dir, "output")
    input_path = os.path.join(data_dir, "input")


    resource_json_filepath = os.path.join(data_dir, "resource.json")
    resource_json_file = open(resource_json_filepath)
    resource_data = json.load(resource_json_file)

    width = 0
    height = 0
    pixels_list = []
    metadata = None

    out_name = argv[0]
    argv = argv[1:]

    for png_id in argv:
        png_founded = get_resource_data(resource_data, png_id, "")
        png_path = os.path.join(input_path, png_founded["FilePath"])
        r = png.Reader(filename=png_path)
        w, h, p, m = r.read_flat()
        width = w
        height = h
        pixels_list.append(p)
        metadata = m

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

    pixels = alphablend(pixels_list[0], pixels_list[1], width, height)

    for idx in range(2, len(pixels_list)):
        pixels = alphablend(pixels, pixels_list[idx], width, height)

    png_out = os.path.join(output_path, out_name + ".png")
    f = open(png_out, 'wb')
    w = png.Writer(width, height, **metadata)
    w.write_array(f, pixels)
    f.close()



if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    try:
        merge(argv)
    except ConfigNotFoundError as e:
        print(e)
        raise