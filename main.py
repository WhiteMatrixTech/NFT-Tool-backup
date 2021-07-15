import bpy
import sys
import os
import json
import better_fbx

TYPE_PAWN = "Pawn"
TYPE_SCENE = "Scene"
TYPE_PLACE = "Place"
TYPE_PART = "Part"
TYPE_WHOLE = "Whole"

pawn_data_format = ["tokenId", "id", "hat", "head", "jacket", "trousers", "shoes", "type"]
composite_data_format = ["target", "pawns"]
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')

class ConfigNotFoundError(Exception):
    pass

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

def get_composition_data(composition_data, data_id, data_type=None):
    composition_data_founded = None
    for c in composition_data:
        c_id = round(c["ID"])
        if c_id == data_id:
            if (data_type != None) and (c["Type"] == data_type):
                composition_data_founded = c
                break
            else:
                composition_data_founded = c
                break

    if composition_data_founded == None:
        raise ConfigNotFoundError("composition data not found ! please check composition.xls or run generate_config script! ID : " + str(data_id))

    return composition_data_founded


def get_resource_data(resource_data, data_id, data_category=None):
    res_founded = None
    for r in resource_data:
        r_id = round(r["ID"])
        if r_id == data_id:
            if (data_category != None) and (r["Category"] == data_category):
                res_founded = r
                break
            else:
                res_founded = r
                break

    if res_founded == None:
        raise ConfigNotFoundError("resource data not found ! please check resource.xls or run generate_config script! ID : " + str(data_id))

    return res_founded


def make_pawn(global_config, composition_data, resource_data, pawn_param, apply_pose):
    pawn_id = pawn_param["id"]

    composition_data_founded = get_composition_data(composition_data, pawn_id, TYPE_PAWN)

    armature_obj = None

    # components

    component_objects = []
    components = pawn_data_format[2:]
    for comp_name in components:
        comp_id = pawn_param[comp_name]
        if comp_id == -1:
            continue

        res_founded = get_resource_data(resource_data, comp_id, comp_name)

        comp_filepath = os.path.abspath(os.path.join(data_dir, "input", res_founded["FilePath"]))
        bpy.ops.import_scene.fbx( filepath = comp_filepath, automatic_bone_orientation = True, force_connect_children = True )
        #better_fbx.fuck_fbx(bpy.context, comp_filepath)
        component_objects.extend(bpy.context.selected_objects[:])

        #if(comp_name == "type"):
        #    for comp_obj in bpy.context.selected_objects[:]:
        #        if comp_obj.type == "ARMATURE":
        #            armature_obj = comp_obj
        #            break

    # material

    for obj in component_objects:
        if obj.type != "MESH":
            continue
        generic_mat = bpy.data.materials.get("GenericMaterial").copy()
        if obj.data.materials:
            using_mat = obj.data.materials[0]
            tex_image_node = using_mat.node_tree.nodes["Image Texture"]
            using_tex = tex_image_node.image

            generic_mat.node_tree.nodes["Image Texture"].image = using_tex
            obj.data.materials[0] = generic_mat

    # pose 

    if apply_pose == True:

        for action in bpy.data.actions:
            bpy.data.actions.remove(action)

        pose_id = round(composition_data_founded["Pawn_PoseID"])

        res_founded = get_resource_data(resource_data, pose_id, "Pose")

        pose_filepath = os.path.abspath(os.path.join(data_dir, "input", res_founded["FilePath"]))
        bpy.ops.import_scene.fbx( filepath = pose_filepath, automatic_bone_orientation = True, force_connect_children = True )
        pose_objects = bpy.context.selected_objects[:]

        for pose_obj in pose_objects:
            if pose_obj.type == "ARMATURE":
                armature_obj = pose_obj
                break

        bpy.ops.object.select_all(action='DESELECT')

        action_to_apply = bpy.data.actions[0]

        for comp_obj in component_objects:
            if comp_obj.type == "ARMATURE":
                comp_obj.animation_data_clear()
                if(comp_obj.animation_data == None):
                    comp_obj.animation_data_create()
                comp_obj.animation_data.action = action_to_apply
                #bpy.context.view_layer.objects.active = comp_obj

        bpy.context.scene.frame_set(2)

        #bpy.ops.object.select_all(action='DESELECT')
        #for pose in pose_objects:
        #    pose.select_set(True)
        #bpy.ops.object.delete()

    # item
    
    item_objects = []

    if apply_pose == True:

        item_lefthand = -1
        item_righthand = -1
        if(composition_data_founded["Pawn_LeftHandID"] != ""):
            item_lefthand = round(composition_data_founded["Pawn_LeftHandID"])
        if(composition_data_founded["Pawn_RightHandID"] != ""):
            item_righthand = round(composition_data_founded["Pawn_RightHandID"])

        def apply_item(item_id, attach_bone):
            bpy.ops.object.select_all(action='DESELECT')
            res_founded = get_resource_data(resource_data, item_id, "Prop")
            item_filepath = os.path.abspath(os.path.join(base_dir, "data", "input", res_founded["FilePath"]))
            bpy.ops.import_scene.fbx( filepath = item_filepath )
            #better_fbx.fuck_fbx(bpy.context, item_filepath)
            current_item_objects = bpy.context.selected_objects[:]
            item_objects.extend(current_item_objects)
            if(res_founded["Scale"] != ""):
                for item_obj in current_item_objects:
                    item_obj.scale = (float(res_founded["Scale"]), float(res_founded["Scale"]), float(res_founded["Scale"]))

            item_obj = current_item_objects[0]
            #for item_obj in current_item_objects:
            #bpy.context.view_layer.objects.active = item_obj
            #print(item_obj)
            #c = item_obj.constraints.new(type='CHILD_OF')
            #print("111111111111111111111111111111")
            #c.target = bpy.data.objects["Bip001.005"]
            #print(armature_obj)
            #c.subtarget = attach_bone
            #print(attach_bone)
            bpy.ops.object.select_all(action='DESELECT')
            armature_obj.select_set(True)
            bone_matrix = armature_obj.matrix_world @ armature_obj.pose.bones[attach_bone].matrix
            item_obj.location = bone_matrix.to_translation()
            item_obj.rotation_euler = bone_matrix.to_euler()




        if item_lefthand != -1:
            apply_item(item_lefthand, "b_LWeapon")

        if item_righthand != -1:
            apply_item(item_righthand, "b_RWeapon")


    bpy.ops.object.select_all(action='DESELECT')

    for item_obj in item_objects:
        item_obj.select_set(True)

    for comp_obj in component_objects:
        comp_obj.select_set(True)
    
    return True


def make_composite(global_config, composition_data, resource_data, composite_param):
    target_id = composite_param["target"]
    
    composite_tree = {}
    composite_tree["ID"] = target_id
    composite_tree["IsRoot"] = 1

    def construct(node, root_position):
        node_id = node["ID"]

        node_composition_data_founded = get_composition_data(composition_data, node_id)

        node["Type"] = node_composition_data_founded["Type"]
        node_world_pos = eval(node_composition_data_founded["Position"])

        if "IsRoot" in node:
            root_position = node_world_pos
            node["Position"] = [0, 0, 0]
        else:
            node["Position"] = [node_world_pos[0] - root_position[0], node_world_pos[1] - root_position[1], node_world_pos[2] - root_position[2]]

        if node["Type"] == TYPE_SCENE:
            # load scene file
            scene_res_id = node_composition_data_founded["Scene_ResID"]
            res_founded = get_resource_data(resource_data, scene_res_id, TYPE_SCENE)

            scene_res_filepath = os.path.abspath(os.path.join(data_dir, "input", res_founded["FilePath"]))
            bpy.ops.import_scene.fbx( filepath = scene_res_filepath, automatic_bone_orientation = True, force_connect_children = True )
            scene_objects = bpy.context.selected_objects[:]
            for scene_object in scene_objects:
                scene_object.location = (node["Position"][0], node["Position"][1], node["Position"][2])

        if node["Type"] == TYPE_PAWN:
            # load pawn file
            pawn_id = node["ID"]
            pawn_token_id = None
            for pawn_data in composite_param["pawns"]:
                if pawn_id == pawn_data["id"] :
                    pawn_token_id = pawn_data["tokenId"]
                    break
            
            pawn_filepath = os.path.abspath(os.path.join(data_dir, "output", TYPE_PAWN ,str(pawn_id), TYPE_PAWN + "_" + str(pawn_token_id) + ".glb"))
            if os.path.isfile(pawn_filepath) == False:
                print("pawn file not found ! please generate this pawn before composite  ID : " + str(pawn_id) + " tokenId : " + str(pawn_token_id) + " Path :" + str(pawn_filepath))
                return
            
            bpy.ops.import_scene.gltf( filepath = pawn_filepath, bone_heuristic = 'BLENDER')
            pawn_objects = bpy.context.selected_objects[:]
            for pawn_object in pawn_objects:
                pawn_object.location = (node["Position"][0], node["Position"][1], node["Position"][2])
            
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
            construct(child_node, root_position)

    construct(composite_tree, [0, 0, 0])

    return



def export_picture(export_filepath, resolution_2d):
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath = export_filepath
    bpy.context.scene.render.resolution_x = resolution_2d["x"]
    bpy.context.scene.render.resolution_y = resolution_2d["y"]
    bpy.ops.render.render(write_still=True)

def export_model(export_filepath):
    bpy.ops.export_scene.gltf(filepath = export_filepath, use_selection = True, export_materials = 'EXPORT', export_animations = False, export_current_frame = True, export_skins = True)


def main(argv):
    output_path = os.path.join(data_dir, "output")
    output_mode = int(argv[0])
    input_param = json.loads(argv[1])

    bpy.ops.preferences.addon_enable(module='better_fbx')
    bpy.ops.script.reload()

    environment_blend_file = os.path.join(data_dir, "input", "environment.blend")
    bpy.ops.wm.open_mainfile(filepath = environment_blend_file)

    #comp_filepath = os.path.abspath(os.path.join(base_dir, "input", "test617/HEAD/A59_HEAD_zongzi.FBX"))
    #bpy.ops.import_scene.fbx( filepath = comp_filepath, automatic_bone_orientation = True, force_connect_children = True )
    #better_fbx.fuck_fbx(bpy.context, comp_filepath)

    composition_json_filepath = os.path.join(data_dir, "composition.json")
    composition_json_file = open(composition_json_filepath)
    composition_data = json.load(composition_json_file)

    resource_json_filepath = os.path.join(data_dir, "resource.json")
    resource_json_file = open(resource_json_filepath)
    resource_data = json.load(resource_json_file)

    config_json_filepath = os.path.join(data_dir, "config.json")
    config_json_file = open(config_json_filepath)
    global_config = json.load(config_json_file)

    # delete the default cube
    #objs = bpy.data.objects
    #objs.remove(objs["Cube"], do_unlink=True)

    # make and export
    if (output_mode == 0) or (output_mode == 1):
        pawn_param = input_param
        if check_pawn_param(pawn_param) == False :
            return

        make_successed = make_pawn(global_config, composition_data, resource_data, pawn_param, output_mode == 1)
        if make_successed == True:
            #make dir
            pawn_dir = os.path.join(output_path, "pawn", str(pawn_param["id"]))
            if not os.path.exists(pawn_dir):
                os.makedirs(pawn_dir)

            #model
            pawn_model_filename = TYPE_PAWN + "_" + str(pawn_param["tokenId"]) + ".glb"
            pawn_model_filepath = os.path.join(pawn_dir, pawn_model_filename)
            export_model(pawn_model_filepath)

            #picture
            pawn_picture_filename = TYPE_PAWN + "_" + str(pawn_param["tokenId"]) + ".png"
            pawn_picture_filepath = os.path.join(pawn_dir, pawn_picture_filename)
            resolution_2d = global_config["Resolution"][TYPE_PAWN]
            export_picture(pawn_picture_filepath, resolution_2d)

            

    
    if (output_mode == 2):
        composite_param = input_param
        if check_composite_param(composite_param) == False :
            return

        make_composite(global_config, composition_data, resource_data, composite_param)

        target_id = composite_param["target"]
        composition_data_founded = get_composition_data(composition_data, target_id)
        target_type = composition_data_founded["Type"]

        #picture
        composite_picture_filename = target_type + "_" + str(composite_param["tokenId"]) + ".png"
        composite_picture_filepath = os.path.join(output_path, target_type.lower(), composite_picture_filename)
        resolution_2d = global_config["Resolution"][target_type]
        export_picture(composite_picture_filepath, resolution_2d)

        #model
        #composite_model_filename = target_type + "_" + composite_param["tokenId"] + ".glb"
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
    except ConfigNotFoundError as e:
        print(e)
        raise
