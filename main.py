import bpy
import sys
import os
import json

pawn_data_format = ["ID", "Hat", "Head", "Jacket", "Trousers", "Shoes", "Type"]

def check_pawn_param(pawn_param):
    for k in pawn_data_format:
        if k not in pawn_param:
            print("input format error : " + k + " not found")
            return False
    return True

def make_pawn(composition_data, resource_data, pawn_param, apply_pose):
    pawn_id = pawn_param["ID"]

    composition_data_founded = None
    for c in composition_data:
        c_id = round(c["ID"])
        if((c_id == pawn_id) and (c["Type"] == "Pawn")):
            composition_data_founded = c
    
    if composition_data_founded == None:
        print("composition data not found ! please check composition.xls or run generate_config script! ID : " + pawn_id)
        return False

    pose_id = round(composition_data_founded["Pawn_PoseID"])
    item_lefthand = round(composition_data_founded["Pawn_LeftHandID"])
    item_righthand = round(composition_data_founded["Pawn_RightHandID"])

    components = pawn_data_format[1:]
    for comp_name in components:

        comp_id = pawn_param[comp_name]

        if comp_id == -1:
            continue

        res_founded = None
        for r in resource_data:
            r_id = round(r["ID"])
            if((r_id == comp_id) and (r["Category"] == comp_name)):
                res_founded = r

        if res_founded == None:
            print("resource data not found ! please check resource.xls or run generate_config script! ID : " + comp_id)
            return False

        comp_filepath = os.path.abspath(os.path.join(base_dir, "input",res_founded["FilePath"]))
        bpy.ops.import_scene.fbx( filepath = component_filepath )
        
    
    return True


def make_composite():



def main(argv):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    output_path = os.path.join(base_dir, "output", argv[0])
    output_mode = argv[1]
    #print(argv[2])
    input_param = json.loads(argv[2])
    #print(input_param)

    composition_json_filepath = os.path.join(base_dir, "composition.json")
    composition_json_file = open(composition_json_filepath)
    composition_data = json.load(composition_json_file)

    resource_json_filepath = os.path.join(base_dir, "resource.json")
    resource_json_file = open(resource_json_filepath)
    resource_data = json.load(resource_json_file)

    # delete the default cube
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)

    make_successed = False
    if (output_mode == 0) or (output_mode == 1):
        pawn_param = input_param
        if(check_pawn_param(pawn_param) == False):
            return
        make_successed = make_pawn(composition_data, resource_data, pawn_param, output_mode == 1)
    
    if (output_mode == 2):
        make_successed = make_composite()

    if make_successed == True:
        # do export

    #for component_id in component_id_list:
    #    if component_id not in config.components:
    #        print("ERROR : component id " + component_id + " not exist. please check config.py ")
    #        return

    #    if "filepath" not in config.components[component_id]:
    #        print("ERROR : component id " + component_id + " filepath not exist. please check config.py ")
    #        return
    #    
    #    component_filepath = os.path.abspath(os.path.join(base_dir, "input", config.components[component_id]["filepath"]))
    #    bpy.ops.import_scene.fbx( filepath = component_filepath )

    # make some modification on the components
    # ...

    # apply animation pose
    


    # apply camera setting



    # export target file

    
    #if(output_mode == "0" or output_mode == "1"):
    #    # export picture
    #    pic_output_path = output_path + ".png"
    #    print("exporting " + pic_output_path + " ...")

    #    bpy.context.scene.render.image_settings.file_format='PNG'
    #    bpy.context.scene.render.filepath = pic_output_path
    #    bpy.context.scene.render.resolution_x = config.render_solution["x"]
    #    bpy.context.scene.render.resolution_y = config.render_solution["y"]
    #    bpy.ops.render.render(write_still=True)
    #
    #if(output_mode == "0" or output_mode == "2"):
    #    # export glb
    #    glb_output_path = output_path + ".glb"
    #    print("exporting " + glb_output_path + " ...")
    #    bpy.ops.export_scene.gltf(filepath = glb_output_path)



    # do some cleaning
    composition_json_file.close()
    resource_json_file.close()

if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    try:
        main(argv)
    except Exception as e:
        print(e)


