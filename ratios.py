#!/usr/bin/env python
from collections import namedtuple
import json
import argparse

DATA_FILE = 'recipes_bobs_mods_and_others_12232020.json'

with open(DATA_FILE, 'r') as f:
    data = json.load(f)

Recipe = namedtuple('Recipe',
                    'ingredients,craft_time,machine_type,count,name')

Machine = namedtuple('Machine',
                     'machine_type,craft_speed,name')

# TODO: unsure if all of these are valid...
ALIASES = {
    'advanced-crafting': 'crafting',  # engine only?
    'crafting-machine': 'crafting',
    'electronics-machine': 'electronics'
}
# TODO(machines): barrelling; crafting-with-fluid;
MACHINE_T_LOOKUP = {
    'air-pump': [
        'air-pump',
        'air-pump-2',
        'air-pump-3',
        'air-pump-4',
    ],
    'crafting': [
        'assembling-machine-1',
        'assembling-machine-2',
        'assembling-machine-3',
        'assembling-machine-4',
        'assembling-machine-5',
        'burner-assembling-machine',
        'steam-assembling-machine',
        'assembling-machine-6'],
    'distillery': [
        'bob-distillery',
        'bob-distillery-2',
        'bob-distillery-3',
        'bob-distillery-4',
        'bob-distillery-5'
    ],
    'bob-greenhouse': ['bob-greenhouse'],
    'centrifuging': [
        'centrifuge',
        'centrifuge-2',
        'centrifuge-3',
    ],
    'chemistry': [
        'chemical-plant',
        'chemical-plant-2',
        'chemical-plant-3',
        'chemical-plant-4',
    ],
    'chemical-furnace': [
        'fluid-chemical-furnace',
        'steel-chemical-furnace',
        'stone-chemical-furnace',
        'electric-chemical-furnace',
        'electric-chemical-mixing-furnace',
        'electric-chemical-mixing-furnace-2',
    ],
    'smelting': [
        'electric-furnace',
        'electric-furnace-2',
        'stone-furnace',
        'fluid-furnace',
        'steel-furnace',
        'electric-furnace-3',
    ],
    'mixing-furnace': [
        'electric-mixing-furnace',
        'steel-mixing-furnace',
        'stone-mixing-furnace',
        'fluid-mixing-furnace',
    ],
    'electrolysis': [
        'electrolyser',
        'electrolyser-2',
        'electrolyser-3',
        'electrolyser-4',
        'electrolyser-5',
    ],
    'electronics': [
        'electronics-machine-1',
        'electronics-machine-2',
        'electronics-machine-3'
    ],
    'oil-processing': [
        'oil-refinery',
        'oil-refinery-2',
        'oil-refinery-3',
        'oil-refinery-4'
    ],
    'rocket-building': ['rocket-silo'],
    'void-fluid': ['void-pump'],
    # 'water-pump',
    # 'water-pump-2',
    # 'water-pump-3',
    # 'water-pump-4'
}
# reverse...
MACHINE_T_LOOKUP_REV = {vv: k
                        for k, v in MACHINE_T_LOOKUP.items()
                        for vv in v}

def solve(item, rate, machines, ignore, indent=0):
    # count: items per second
    spaces = ' ' * indent
    if type(item) is str:
        print(spaces + item, f'({rate:.2f}/s)', '?')
        return
    if item in ignore:
        print(spaces + item.name, f'({rate:.2f}/s)', '?')
        return
    # calc times needed to be crafted per second
    # figure out best machine
    m_ok = [m for m in machines if m.machine_type in item.machine_type]
    assert m_ok, 'no valid machines available'
    m_best = max(m_ok, key=lambda m: m.craft_speed)
    # figure out number of machines needed
    crafts_needed = rate / (item.count *
                            m_best.craft_speed / item.craft_time)
    # print(spaces + f'-- start {item.name} --')
    print(spaces + item.name, f'({rate:.2f}/s)', '|', m_best.name, 'x',
          crafts_needed)

    for ing in item.ingredients:
        if type(ing) is tuple:
            solve(ing[0], crafts_needed * ing[1] / item.craft_time,
                  machines, ignore, indent + 2)
        else:
            solve(ing, crafts_needed / item.craft_time,
                  machines, ignore, indent + 2)
    # print(spaces + f'-- end {item.name} --')


parser = argparse.ArgumentParser(  # noqa
    description='Factorio recipe calculator',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument('--rate', '-r', type=float, default=1,
                    help='rate of production of target recipe')
parser.add_argument('--recipe', '-R', required=True,
                    help='the recipe to make')
parser.add_argument('--ignore', '-i', nargs='+', default=(),
                    help='do not show ingredients for these recipes')

args = parser.parse_args()

# recipe = basic_circuit_board
# recipe = transport_belt
recipe = eval(args.recipe)

avail_machines = [ass1, ass2, elec1, mm1, cf1, cp1]
rate = args.rate  # items per second
ignore = [eval(i) for i in args.ignore]

solve(recipe, rate, avail_machines, ignore)
