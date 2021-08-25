import json
import re

from generate_random_pawn import parse_csv_to_nft_component_info

TRAITS_V1 = parse_csv_to_nft_component_info('./fusion_config_08_12.csv')
TRAITS_V2 = parse_csv_to_nft_component_info('./fusion_config_08_14.csv')

TRAIT_TABLE_V1 = {item.globalId: item for item in TRAITS_V1}
TRAIT_TABLE_V2 = {item.globalId: item for item in TRAITS_V2}

print(TRAIT_TABLE_V1)
print(TRAIT_TABLE_V2)

RARITY_MAP = {
    'n': 'Normal',
    'r': 'Rare',
    'sr': 'Super Rare',
    'na': None
}


def get_failed_items():

    failed = set()

    for i in range(10):
        file_name = 'logs_{}_to_{}.txt'.format(i * 1000 + 1, i * 1000 + 1000)
        with open(file_name, 'r') as f:
            for line in f.readlines():
                if 'not found' in line:
                    # print(line)
                    m = re.search('Pawn_(\d+)', line)
                    failed.add(int(m.groups(0)[0]))

    return failed


def get_traits_for_item(item):
    traits = []
    if item['version'] == 1:
        trait_table = TRAIT_TABLE_V1
    else:
        trait_table = TRAIT_TABLE_V2
    for key in item:
        if key == 'version' or key == 'signature':
            continue

        trait_info = trait_table[item[key]]
        trait_type = trait_info.type
        if trait_type.lower() == 'image':
            trait_type = 'background'
        if trait_type.lower() == 'type' or trait_type == 'background':
            normalized_trait = trait_info.resourceName
        else:
            normalized_trait = re.sub(" \d+", " ", trait_info.resourceName).strip()

        trait_type = trait_type.title()
        traits.append({
            "trait_type": trait_type,
            "value": normalized_trait
        })
        rarity_value = RARITY_MAP[trait_info.rarity]
        if rarity_value:
            traits.append({
                "trait_type": trait_type + ' Rarity',
                "value": rarity_value
            })
        print(traits)

    item['traits'] = traits


def get_traits():
    with open('appearance_0814.json', 'r') as a:
        f1 = json.load(a)
        print(len(f1))

    with open('appearance.json', 'r') as b:
        f2 = json.load(b)
        print(len(f2))

    failed_items = get_failed_items()

    all_items_with_traits = []

    for idx, item in enumerate(f1):
        item_to_add = item
        # print(item_to_add)
        if item['signature'] not in failed_items:
            item['version'] = 2
        else:
            print(item, 'failed, will find in another file')
            item_backup = f2[idx]
            item_backup['version'] = 2
            item_to_add = item_backup
            print('added', item_backup, 'to all items')
        try:
            get_traits_for_item(item_to_add)
        except KeyError as e:
            print('error:')
            print(e)
        all_items_with_traits.append(item_to_add)
    print(all_items_with_traits[0])
    return all_items_with_traits


all_items_with_traits = get_traits()
with open("all_item_with_traits_0818.json", "w") as json_file:
    json.dump(all_items_with_traits, json_file)
