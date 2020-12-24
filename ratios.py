#!/usr/bin/env python
from collections import namedtuple
import json
import argparse
import re

DATA_FILE = 'recipes_bobs_mods_and_others_12232020.json'

with open(DATA_FILE, 'r') as f:
    data = json.load(f)

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
    'water-pump': [
        'water-pump',
        'water-pump-2',
        'water-pump-3',
        'water-pump-4',
    ]
}
# reverse...
MACHINE_T_LOOKUP_REV = {vv: k
                        for k, v in MACHINE_T_LOOKUP.items()
                        for vv in v}

Recipe = namedtuple('Recipe',
                    'ingredients,craft_time,machine_type,count,name')

Machine = namedtuple('Machine',
                     'machine_type,craft_speed,name')

recipes = {}
machines = {}

for item, meta in data.items():
    products = meta['products']
    if len(products) != 1 or products[0]['name'] != meta['name']:
        # print('Unsupported: skipping', item)  # TODO!!!
        continue

    recipes[item] = Recipe(
        ingredients=[(v['name'], v['amount']) for v in meta['ingredients']],
        craft_time=meta['energy'],  # energy is time in seconds...
        machine_type=ALIASES.get(meta['category'], meta['category']),
        count=products[0]['amount'],
        name=meta['name'],
    )

    if 'speed' in meta:
        machines[item] = Machine(
            machine_type=MACHINE_T_LOOKUP_REV[item],
            craft_speed=meta['speed'],
            name=meta['name'],
        )


def solve(item, rate, machines, ignore, indent=0, sep=''):
    # count: items per second
    spaces = sep[:-2] + '|_' if sep else ''
    if item in ignore or item not in recipes:
        print(spaces + item, f'({rate:.2f}/s)', '<ignored>')
        return

    item = recipes[item]
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

    for i, ing in enumerate(item.ingredients):  # ing should be a tuple...
        sep_next = (sep + '  ' if (i + 1) == len(item.ingredients) else
                    sep + '| ')

        solve(ing[0], crafts_needed * ing[1] / item.craft_time,
              machines, ignore, indent + 2, sep_next)

parser = argparse.ArgumentParser(  # noqa
    description='Factorio recipe calculator',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument('--rate', '-r', type=float, default=1,
                    help='rate of production of target recipe')
parser.add_argument('--recipe', '-R', required=True,
                    help='the recipe to make')
parser.add_argument('--ignore', '-i', nargs='+', default=[],
                    help='do not show ingredients for these recipes')
parser.add_argument('--ignore-basic', '-I', action='store_true',
                    help='ignore basic items you have on your bus, probably')

args = parser.parse_args()

recipe = args.recipe

# TODO: this is hard-coded...maybe move to config file
avail_machines = [
    'assembling-machine-1',
    'assembling-machine-2',
    'chemical-plant',
    'electronics-machine-1',
    'bob-distillery',
    'stone-mixing-furnace',
    'steel-mixing-furnace',
    'stone-chemical-furnace',
    'steel-chemical-furnace',
    'steel-furnace',
]
avail_machines = [machines[m] for m in avail_machines]
rate = args.rate  # items per second
ignore = args.ignore

if args.ignore_basic:
    partial_words = ['plate']
    # whole_words = ['coal']
    re_base = r'([^a-zA-Z]|^){}([^a-zA-Z]|$)'
    rx_ignore = re.compile(
        '(' + '|'.join(re_base.format(pw) for pw in partial_words) + ')'
    )
    ignore.extend(
        r for r in recipes if rx_ignore.search(r)
    )

solve(recipe, rate, avail_machines, ignore)
