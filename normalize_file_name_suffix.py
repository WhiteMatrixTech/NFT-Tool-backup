import json
from pathlib import Path


def batch_renaming():
    for path in Path('./data/input').rglob('*.*'):
        has_upper = any(ele.isupper() for ele in path.name)
        if has_upper:
            print('renaming ' + path.name)
            path.rename(str(path.parent.absolute()) + '/' + path.name.lower())


def normalize_resource_json():
    with open('./data/resource.json') as json_file:
        resource_json = json.load(json_file)
        for row in resource_json:
            path = row['FilePath']
            parent_folder = path[:path.rindex('/')]
            file_name = path[path.rindex('/'):]
            normalized_path = parent_folder + file_name.lower()
            print('renaming ' + path)
            row['FilePath'] = normalized_path
    with open("./data/resource.json", "w") as json_file:
        json.dump(resource_json, json_file)


batch_renaming()
normalize_resource_json()