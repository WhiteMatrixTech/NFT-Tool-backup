import sys
from dataclasses import dataclass
from numpy.random import default_rng
import numpy as np
from dataclass_csv import DataclassReader
import json
import subprocess
from pathlib import Path


@dataclass
class NFTComponentInfo:
    globalId: int
    resourceName: str
    probability: float
    type: str
    rarity: str
    hairColor: int = 0  # 0: false, 1: true
    exclusiveGroupIds: str = ''  # '1,13,14,15,16,17,18,19'


@dataclass
class RarityComboInfo:
    nCount: int
    rCount: int
    srCount: int


@dataclass
class RarityComboLevelInfo:
    level: int
    probability: float
    combos: list


COMBO_DATA = [
    RarityComboLevelInfo(
        1, 26,
        [
            RarityComboInfo(6, 0, 0),
            RarityComboInfo(5, 1, 0),
        ]
    ),
    RarityComboLevelInfo(
        2, 20,
        [
            RarityComboInfo(5, 0, 1),
            RarityComboInfo(4, 2, 0),
            RarityComboInfo(4, 1, 1),
        ]
    ),
    RarityComboLevelInfo(
        3, 15,
        [
            RarityComboInfo(3, 3, 0),
            RarityComboInfo(4, 0, 2),
            RarityComboInfo(3, 2, 1),
        ]
    ),
    RarityComboLevelInfo(
        4, 13,
        [
            RarityComboInfo(3, 1, 2),
            RarityComboInfo(3, 0, 3),
            RarityComboInfo(2, 4, 1),
        ]
    ),
    RarityComboLevelInfo(
        5, 10,
        [
            RarityComboInfo(2, 3, 1),
            RarityComboInfo(2, 2, 2),
            RarityComboInfo(2, 1, 3),
        ]
    ),
    RarityComboLevelInfo(
        6, 7,
        [
            RarityComboInfo(2, 0, 4),
            RarityComboInfo(1, 5, 2),
            RarityComboInfo(1, 4, 1),
        ]
    ),
    RarityComboLevelInfo(
        7, 5,
        [
            RarityComboInfo(1, 3, 2),
            RarityComboInfo(1, 2, 3),
            RarityComboInfo(0, 3, 3),
        ]
    ),
    RarityComboLevelInfo(
        8, 3,
        [
            RarityComboInfo(1, 1, 4),
            RarityComboInfo(0, 2, 4),
            RarityComboInfo(2, 0, 4),
        ]
    ),
    RarityComboLevelInfo(
        9, 1,
        [
            RarityComboInfo(1, 0, 5),
            RarityComboInfo(0, 1, 5),
            RarityComboInfo(0, 0, 6),
        ]
    ),
]


class ProbInfoPairArray:

    def __init__(self, total_prob):
        self.probs = []
        self.items = []
        self.total_prob_calculator = 0
        self.total_prob = total_prob
        self.frozen = False

    def add_item(self, item):
        if self.frozen:
            raise Exception('Pair Array is frozen')
        if self.total_prob < self.total_prob_calculator + item.probability:
            raise ValueError(
                'total_prob {} < total_prob_calculator {}'.format(self.total_prob,
                                                                  self.total_prob_calculator + item.probability))

        self.items.append(item)
        self.total_prob_calculator += item.probability
        self.probs.append(item.probability)

    def freeze(self):
        if self.total_prob != self.total_prob_calculator:
            raise ValueError(
                'total_prob {} != total_prob_calculator {}'.format(self.total_prob, self.total_prob_calculator))
        self.frozen = True

    def get_items(self):
        return self.items

    def get_probs(self):
        return self.probs


class RarityComboManager:

    def __init__(self, combo_level_infos):
        self.combo_level_infos = combo_level_infos
        self.level_prob = [level.probability for level in combo_level_infos]

    def generate_rarity_combo(self, rng):
        chosen_level = rng_choice(rng, self.combo_level_infos, 1, self.level_prob)[0]
        chosen_combo = rng.choice(chosen_level.combos, 1)[0]
        rarities = []
        for i in range(chosen_combo.nCount):
            rarities.append('n')
        for i in range(chosen_combo.rCount):
            rarities.append('r')
        for i in range(chosen_combo.srCount):
            rarities.append('sr')
        rng.shuffle(rarities)
        return rarities


class ProbManager:

    def __init__(self, component_infos):
        self.rarity_type_prob_map = {}
        self.type_to_hat_offset_map = {
            'X01_body_Type1': 0,
            'X02_body_Type2': 1,
            'X03_body_Type3': 2,
            'X04_body_Type4': 3,
            'X05_body_Type5': 4,
            'X06_body_Type6': 5,
        }
        for component_info in component_infos:
            key = self.build_key(component_info.rarity, component_info.type)
            if key not in self.rarity_type_prob_map:
                self.rarity_type_prob_map[key] = ProbInfoPairArray(1000)
            self.rarity_type_prob_map[key].add_item(component_info)

        for v in self.rarity_type_prob_map.values():
            v.freeze()

    @staticmethod
    def build_key(rarity, component_type):
        return rarity + '-' + component_type

    def resolve_hat_component(self, type_info, hat_info):
        if hat_info.hairColor == 0:
            return hat_info.globalId
        return hat_info.globalId + self.type_to_hat_offset_map[type_info.resourceName]

    def get_prob_info_pair_array(self, rarity, type):
        return self.rarity_type_prob_map[self.build_key(rarity, type)]

    def randomly_generate_component(self, rng, rarity, type):
        prob_info_pair_array = self.get_prob_info_pair_array(rarity, type)
        return rng_choice(rng, prob_info_pair_array.get_items(), 1, prob_info_pair_array.get_probs())[0]


def rng_choice(rng, choices, count, probs):
    f64probs = np.asarray(probs).astype('float64')
    normalized_probs = f64probs / np.sum(f64probs)
    return rng.choice(choices, count, p=normalized_probs)


def parse_csv_to_nft_component_info(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as nft_component_csv:
        reader = DataclassReader(nft_component_csv, NFTComponentInfo)
        infos = []
        for data in reader:
            data.type = data.type.lower()
            infos.append(data)
        return infos


RARITY_RELATED_COMBO_COMPONENTS = [
    'type', 'hat', 'head', 'jacket', 'trousers', 'shoes'
]


def provide_combo_manager():
    return RarityComboManager(COMBO_DATA)


def provide_prob_manager(file_path):
    nft_infos = parse_csv_to_nft_component_info(file_path)
    return ProbManager(nft_infos)


def generate_nft_appearance_from_signature(signature, location_id, combo_manager, prob_manager):
    rng = default_rng(signature)
    exclusive_ids = set()
    rarity_combo = combo_manager.generate_rarity_combo(rng)
    generated_components = []
    for idx, component in enumerate(RARITY_RELATED_COMBO_COMPONENTS):
        info = None
        while True:
            info = prob_manager.randomly_generate_component(rng, rarity_combo[idx],
                                                            RARITY_RELATED_COMBO_COMPONENTS[idx])
            info_exclusive_ids = info.exclusiveGroupIds.split(',')
            if len(info_exclusive_ids) > 0 and info_exclusive_ids != ['']:
                info_exclusive_set = set(map(int, info_exclusive_ids))
            else:
                info_exclusive_set = set()
            if info and set(exclusive_ids).isdisjoint(info_exclusive_set):
                break
        exclusive_ids = exclusive_ids.union(info_exclusive_set)
        generated_components.append(info)
    background = prob_manager.randomly_generate_component(rng, 'na', 'image')
    generated_components.append(background)

    return {
        'tokenId': signature,
        'id': location_id,
        'type': generated_components[0].globalId,
        'hat': prob_manager.resolve_hat_component(generated_components[0], generated_components[1]),
        'head': generated_components[2].globalId,
        'jacket': generated_components[3].globalId,
        'trousers': generated_components[4].globalId,
        'shoes': generated_components[5].globalId,
        'background': generated_components[6].globalId
    }


def log_file_exists(log_file_name, file_to_check):
    file_path = Path(file_to_check)
    with open(log_file_name, 'a') as f:
        if file_path.is_file():
            f.write("{} exists\n".format(file_path))
        else:
            f.write("{} not found\n".format(file_path))


if __name__ == '__main__':
    combo_manager = provide_combo_manager()
    prob_manager = provide_prob_manager('./fusion_config_08_12.csv')

    from_number = int(sys.argv[1])  # inclusive
    to_number = int(sys.argv[2])  # inclusive

    print('rendering from {} to {}'.format(from_number, to_number))

    with open('locationIdSignatureStockInfo.json') as f:
        location_id_sig_json = json.load(f)

    location_id_sig_map = {}
    for location_id_str in location_id_sig_json:
        location_id = int(location_id_str)
        location_id_sig_map[location_id] = location_id_sig_json[location_id_str]

    counter = 1

    log_file_name = 'logs_{}_to_{}.txt'.format(from_number, to_number)
    generated_nfts = []

    # generate all
    for location_id in sorted(location_id_sig_map.keys()):
        # if from_number <= counter <= to_number:
        sigs = location_id_sig_map[location_id]
        for sig in sigs:
            generated_nft = generate_nft_appearance_from_signature(sig, location_id, combo_manager, prob_manager)
            generated_nfts.append(generated_nft)

    # render specific range
    nft_to_render = generated_nfts[from_number-1:to_number]
    for nft_info in nft_to_render:
        nft_string = json.dumps(nft_info)
        print('rendering for {}'.format(nft_string))
        cmd = 'renderjob.sh 1 {} --cycle-device CUDA'.format(json.dumps(nft_string))
        result = subprocess.run(cmd, shell=True, stderr=sys.stderr, stdout=sys.stdout)
        print('rendering result for {}:'.format(nft_string))
        print(result)

        log_file_exists(log_file_name, 'data/output/pawn/{}/Pawn_{}.png'.format(nft_info['id'], nft_info['tokenId']))
        log_file_exists(log_file_name, 'data/output/pawn/{}/Pawn_{}.glb'.format(nft_info['id'], nft_info['tokenId']))
        log_file_exists(log_file_name, 'data/output/pawn/{}/Pawn_{}_np.png'.format(nft_info['id'], nft_info['tokenId']))

