import csv
import json


def read_resources_id_to_fix(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as resources_to_fix_file:
        reader = csv.reader(resources_to_fix_file, delimiter=',', quotechar='|')
        header_skipped = False
        resources_ids = []
        for row in reader:
            if not header_skipped:
                header_skipped = True
                continue
            resources_ids.append(int(row[1]))
        return resources_ids


def load_all_items(file_path):
    with open(file_path, 'r') as all_items_file:
        all_items = json.load(all_items_file)
        return all_items


resources_ids = set(read_resources_id_to_fix('resources_ids_to_fix.csv'))
print(resources_ids)
all_items = load_all_items('all_item_with_traits_0817-c.json')
affected_items =[]
for item in all_items:
    if item['type'] in resources_ids:
        affected_items.append(item)
        continue
    if item['hat'] in resources_ids:
        affected_items.append(item)
        continue
    if item['head'] in resources_ids:
        affected_items.append(item)
        continue
    if item['jacket'] in resources_ids:
        affected_items.append(item)
        continue
    if item['trousers'] in resources_ids:
        affected_items.append(item)
        continue
    if item['shoes'] in resources_ids:
        affected_items.append(item)
        continue
    if item['background'] in resources_ids:
        affected_items.append(item)
        continue
print(len(affected_items))

