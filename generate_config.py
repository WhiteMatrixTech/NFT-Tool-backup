import bpy
import sys
import xls2json
import os

def generate_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    resource_xls_filepath = os.path.join(base_dir ,"data", "resource.xls")
    composition_xls_filepath = os.path.join(base_dir, "data", "composition.xls")

    #pawn_component_json_filepath = os.path.join(base_dir, "pawn_component.json")
    #composition_json_filepath = os.path.join(base_dir, "composition.json")

    xls2json.convert_from_file(resource_xls_filepath)
    xls2json.convert_from_file(composition_xls_filepath)

    print("config file generated")


if __name__ == "__main__":
    generate_config()


