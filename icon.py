import bpy
import sys
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')

def make_icon(argv):
    output_path = os.path.join(data_dir, "output")
    input_hex = argv[0]

    environment_blend_file = os.path.join(data_dir, "input", "env_icon.blend")
    bpy.ops.wm.open_mainfile(filepath = environment_blend_file)

    input_param = input_hex[2:]
    shape = int(input_param[0], 16)
    size = int(input_param[1], 16)

    color_r = int(input_param[2] + input_param[3], 16) / 255
    color_g = int(input_param[4] + input_param[5], 16) / 255
    color_b = int(input_param[6] + input_param[7], 16) / 255

    print(shape, size, color_r, color_g, color_b)

    obj_cube = bpy.data.objects["Cube"]
    obj_icosphere = bpy.data.objects["Icosphere"]
    obj_plane = bpy.data.objects["Plane"]
    obj_triangle = bpy.data.objects["Triangle"]

    obj_list = [obj_cube, obj_icosphere, obj_plane, obj_triangle]

    obj_icosphere.hide_render = not (shape < 5)
    obj_triangle.hide_render = not (shape > 4 and shape < 9)
    obj_cube.hide_render = not (shape > 8 and shape < 13)
    obj_plane.hide_render = not (shape > 12)

    size_scale = 1
    if size < 4:
        size_scale = 1
    elif size < 8:
        size_scale = 1.5
    elif size < 12:
        size_scale = 2
    else:
        size_scale = 2.5

    for obj in obj_list:
        obj.scale[0] = size_scale
        obj.scale[1] = size_scale
        obj.scale[2] = size_scale

    for obj in obj_list:
        if obj.data.materials:
            using_mat = obj.data.materials[0]
            rgb_node = using_mat.node_tree.nodes["RGB"]
            rgb_node.outputs[0].default_value = (color_r, color_g, color_b, 1)


    icon_file_path = os.path.join(output_path, "icon", input_hex + ".png")
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath = icon_file_path
    bpy.context.scene.render.resolution_x = 256
    bpy.context.scene.render.resolution_y = 256
    bpy.ops.render.render(write_still=True)






if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    make_icon(argv)