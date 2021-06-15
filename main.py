import bpy
import sys
import os
import json

CATEGORY_PAWN = "Pawn"
CATEGORY_SCENE = "Scene"
CATEGORY_PLACE = "Place"
CATEGORY_PART = "Part"
CATEGORY_WHOLE = "Whole"

pawn_data_format = ["UID", "ID", "Hat", "Head", "Jacket", "Trousers", "Shoes", "Type"]
composite_data_format = ["Target", "Pawns"]
global_config = {}

def check_pawn_param(pawn_param):
    for k in pawn_data_format:
        if k not in pawn_param:
            print("pawn input format error : " + k + " not found")
            return False
    return True

def check_composite_param(composite_param):
    for k in composite_data_format:
        if k not in composite_param:
            print("composite input format error : " + k + " not found")
            return False
    return True

def make_pawn(composition_data, resource_data, pawn_param, apply_pose):
    pawn_id = pawn_param["ID"]

    composition_data_founded = None
    for c in composition_data:
        c_id = round(c["ID"])
        if((c_id == pawn_id) and (c["Type"] == CATEGORY_PAWN)):
            composition_data_founded = c
    
    if composition_data_founded == None:
        print("composition data not found ! please check composition.xls or run generate_config script! ID : " + pawn_id)
        return False

    # components

    components = pawn_data_format[2:]
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
    
    # pose 

    pose_id = global_config["DefaultPoseID"]
    if apply_pose == True:
        pose_id = round(composition_data_founded["Pawn_PoseID"])


    # item
    
    if apply_pose == True:
        item_lefthand = round(composition_data_founded["Pawn_LeftHandID"])
        item_righthand = round(composition_data_founded["Pawn_RightHandID"])
        
    
    return True


def make_composite(composition_data, resource_data, composite_param):
    target_id = composite_param["Target"]
    
    composite_tree = {}
    composite_tree["ID"] = target_id
    composite_tree["IsRoot"] = 1
    root_position = [0, 0, 0]

    def construct(node):
        node_id = node["ID"]
        node_composition_data_founded = None
        for c in composition_data:
            c_id = round(c["ID"])
            if(c_id == node_id):
                node_composition_data_founded = c

        if node_composition_data_founded == None:
            print("composition data not found ! please check composition.xls or run generate_config script! ID : " + node_id)
            return False

        node["Type"] = node_composition_data_founded["Type"]
        node_world_pos = eval(node_composition_data_founded["Position"])

        if node["IsRoot"] == 1:
            root_position = node_world_pos
            node["Position"] = [0, 0, 0]
        else:
            node["Position"] = [node_world_pos[0] - root_position[0], node_world_pos[1] - root_position[1], node_world_pos[2] - root_position[2]]

        if node["Type"] == CATEGORY_SCENE:
            # load scene file


        if node["Type"] == CATEGORY_PAWN:
            # load pawn file

            
            return

        node["Children"] = []
        for c in composition_data:
            c_id = round(c["ID"])
            c_parent_id = round(c["ParentID"])
            if c_parent_id == node_id:
                child_node = {}
                child_node["ID"] = c_id
                node["Children"].append(child_node)

        for child_node in node["Children"]:
            construct(child_node)

    ret = construct(composite_tree)

    return ret



def export_picture(export_filepath, resolution_2d):
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath = filepath
    bpy.context.scene.render.resolution_x = resolution_2d["x"]
    bpy.context.scene.render.resolution_y = resolution_2d["y"]
    bpy.ops.render.render(write_still=True)

def export_model(export_filepath):
    bpy.ops.export_scene.gltf(filepath = export_filepath)


def main(argv):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    output_path = os.path.join(base_dir, "output")
    output_mode = argv[0]
    input_param = json.loads(argv[1])

    composition_json_filepath = os.path.join(base_dir, "composition.json")
    composition_json_file = open(composition_json_filepath)
    composition_data = json.load(composition_json_file)

    resource_json_filepath = os.path.join(base_dir, "resource.json")
    resource_json_file = open(resource_json_filepath)
    resource_data = json.load(resource_json_file)

    config_json_filepath = os.path.join(base_dir, "config.json")
    config_json_file = open(config_json_filepath)
    global_config = json.load(config_json_file)

    # delete the default cube
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)

    # make and export
    if (output_mode == 0) or (output_mode == 1):
        pawn_param = input_param
        if check_pawn_param(pawn_param) == False :
            return

        make_successed = make_pawn(composition_data, resource_data, pawn_param, output_mode == 1)
        if make_successed == True:
            #picture
            pawn_picture_filename = CATEGORY_PAWN + "_" + pawn_param["UID"] + ".png"
            pawn_picture_filepath = os.path.join(output_path, "pawn", pawn_param["ID"], pawn_picture_filename)
            resolution_2d = global_config["Resolution"][CATEGORY_PAWN]
            export_picture(pawn_picture_filepath, resolution_2d)

            #model
            pawn_model_filename = CATEGORY_PAWN + "_" + pawn_param["UID"] + ".glb"
            pawn_model_filepath = os.path.join(output_path, "pawn", pawn_param["ID"], pawn_model_filename)
            export_model(pawn_model_filepath)

    
    if (output_mode == 2):
        composite_param = input_param
        if check_composite_param(composite_param) == False :
            return

        make_successed = make_composite(composition_data, resource_data, composite_param)

        if make_successed == True:
            target_id = composite_param["Target"]
            composition_data_founded = None
            for c in composition_data:
                c_id = round(c["ID"])
                if(c_id == target_id):
                    composition_data_founded = c
            if composition_data_founded == None:
                print("composition data not found ! please check composition.xls or run generate_config script! ID : " + target_id)
                return

            target_type = composition_data_founded["Type"]

            #picture
            composite_picture_filename = target_type + "_" + composite_param["UID"] + ".png"
            composite_picture_filepath = os.path.join(output_path, target_type.lower(), composite_picture_filename)
            resolution_2d = global_config["Resolution"][target_type]
            export_picture(composite_picture_filepath, resolution_2d)

            #model
            #composite_model_filename = target_type + "_" + composite_param["UID"] + ".glb"
            #composite_model_filepath = os.path.join(output_path, target_type.lower(), composite_model_filename)
            #export_model(composite_model_filepath)


    # do some cleaning
    composition_json_file.close()
    resource_json_file.close()
    config_json_file.close()

if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    try:
        main(argv)
    except Exception as e:
        print(e)


