import bpy
import sys
import config
import os

def main(argv):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    output_path = os.path.join(base_dir, "output", argv[0])
    output_mode = argv[1]
    pose_id = argv[2]
    component_id_list = eval(argv[3])

    # delete the default cube
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)

    # import components file

    for component_id in component_id_list:
        if component_id not in config.components:
            print("ERROR : component id " + component_id + " not exist. please check config.py ")
            return

        if "filepath" not in config.components[component_id]:
            print("ERROR : component id " + component_id + " filepath not exist. please check config.py ")
            return
        
        component_filepath = os.path.abspath(os.path.join(base_dir, "input", config.components[component_id]["filepath"]))
        bpy.ops.import_scene.fbx( filepath = component_filepath )

    # make some modification on the components
    # ...

    # apply animation pose
    


    # apply camera setting



    # export target file

    
    if(output_mode == "0" or output_mode == "1"):
        # export picture
        pic_output_path = output_path + ".png"
        print("exporting " + pic_output_path + " ...")

        bpy.context.scene.render.image_settings.file_format='PNG'
        bpy.context.scene.render.filepath = pic_output_path
        bpy.context.scene.render.resolution_x = config.render_solution["x"]
        bpy.context.scene.render.resolution_y = config.render_solution["y"]
        bpy.ops.render.render(write_still=True)
    
    if(output_mode == "0" or output_mode == "2"):
        # export glb
        glb_output_path = output_path + ".glb"
        print("exporting " + glb_output_path + " ...")
        bpy.ops.export_scene.gltf(filepath = glb_output_path)

if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    main(argv)


