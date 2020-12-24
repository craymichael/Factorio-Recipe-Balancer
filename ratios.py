#!/usr/bin/env python
from collections import namedtuple
from enum import Enum
import argparse

Recipe = namedtuple('Recipe',
                    'ingredients,craft_time,machine_type,count,name')


class MT(Enum):
    Assembly = 1
    Electronics = 2
    MetalMixing = 3
    ChemicalFurnace = 4
    MultiPurposeFurnace = 5
    ChemicalPlant = 6


copper_cable = Recipe(
    ingredients=['copper_plate'],
    craft_time=0.5,
    machine_type={MT.Assembly,
                  MT.Electronics},
    count=2,
    name='Copper Cable',
)

wooden_board = Recipe(
    ingredients=['wood'],
    craft_time=0.5,
    machine_type={MT.Assembly,
                  MT.Electronics},
    count=2,
    name='Wooden Board',
)

basic_circuit_board = Recipe(
    ingredients=[(copper_cable, 3), wooden_board],
    craft_time=1,
    machine_type={MT.Assembly,
                  MT.Electronics},
    count=1,
    name='Basic Circuit Board',
)

iron_gear_wheel = Recipe(
    ingredients=[('iron_plate', 2)],
    craft_time=0.5,
    machine_type={MT.Assembly},
    count=1,
    name='Iron Gear Wheel',
)

iron_pipe = Recipe(
    ingredients=['iron_plate'],
    craft_time=0.5,
    machine_type={MT.Assembly},
    count=1,
    name='Iron Pipe',
)

basic_transport_belt = Recipe(
    ingredients=['iron_plate', iron_gear_wheel],
    craft_time=0.5,
    machine_type={MT.Assembly},
    count=2,
    name='Basic Transport Belt',
)

transport_belt = Recipe(
    ingredients=[('tin_plate', 2), (iron_gear_wheel, 2), basic_transport_belt],
    craft_time=0.5,
    machine_type={MT.Assembly},
    count=1,
    name='Transport Belt',
)

basic_underground_belt = Recipe(
    ingredients=[('wood', 2), ('stone', 2), (basic_transport_belt, 5)],
    craft_time=1,
    machine_type={MT.Assembly},
    count=2,
    name='Basic Underground Belt',
)

underground_belt = Recipe(
    ingredients=[(iron_gear_wheel, 20), (basic_underground_belt, 2),
                 ('tin_plate', 14)],
    craft_time=1,
    machine_type={MT.Assembly},
    count=2,
    name='Underground Belt',
)

basic_splitter = Recipe(
    ingredients=[('wood', 4), (copper_cable, 4), (basic_transport_belt, 5),
                 (iron_gear_wheel, 2)],
    craft_time=1,
    machine_type={MT.Assembly},
    count=1,
    name='Basic Splitter',
)

splitter = Recipe(
    ingredients=[(iron_gear_wheel, 14), basic_splitter, ('tin_plate', 8),
                 (basic_circuit_board, 5)],
    craft_time=1,
    machine_type={MT.Assembly},
    count=1,
    name='Splitter',
)

resin = Recipe(
    ingredients=['wood'],
    craft_time=1,
    machine_type={MT.Assembly},
    count=1,
    name='Resin',
)

solder_plate = Recipe(
    ingredients=[('tin_plate', 4), ('lead_plate', 7)],
    craft_time=7,
    machine_type={MT.MetalMixing},
    count=11,
    name='Solder Plate',
)

solder = Recipe(
    ingredients=[resin, (solder_plate, 4)],
    craft_time=2,
    machine_type={MT.Assembly, MT.Electronics},
    count=8,
    name='Solder',
)

carbon = Recipe(
    ingredients=['coal', ('water', 5)],
    craft_time=2,
    machine_type={MT.ChemicalFurnace, MT.MultiPurposeFurnace},
    count=2,
    name='Carbon',
)

tinned_copper_wire = Recipe(
    ingredients=[(copper_cable, 3), 'tin_plate'],
    craft_time=0.5,
    machine_type={MT.Assembly, MT.Electronics},
    count=3,
    name='Tinned Copper Wire',
)

basic_electronic_components = Recipe(
    ingredients=[carbon, tinned_copper_wire],
    craft_time=2,
    machine_type={MT.Assembly, MT.Electronics},
    count=5,
    name='Basic Electronic Components',
)

basic_electronic_board = Recipe(
    ingredients=[solder, (basic_electronic_components, 5),
                 basic_circuit_board],
    craft_time=1,
    machine_type={MT.Assembly, MT.Electronics},
    count=1,
    name='Basic Electronic Board',
)

engine_unit = Recipe(
    ingredients=['steel_plate', iron_gear_wheel, (iron_pipe, 2)],
    craft_time=10,
    machine_type={MT.Assembly},
    count=1,
    name='Engine Unit',
)

solar_panel = Recipe(
    ingredients=[('copper_plate', 4), ('steel_plate', 4),
                 (basic_electronic_board, 14)],
    craft_time=10,
    machine_type={MT.Assembly},
    count=1,
    name='Solar Panel',
)

automation_science_pack = Recipe(
    ingredients=['copper_plate', iron_gear_wheel],
    craft_time=5,
    machine_type={MT.Assembly},
    count=1,
    name='Automation Science Pack',
)
yellow_science = automation_science_pack

inserter = Recipe(
    ingredients=['iron_plate', iron_gear_wheel, basic_circuit_board],
    craft_time=0.5,
    machine_type={MT.Assembly},
    count=1,
    name='Inserter',
)

automation_science_pack = Recipe(
    ingredients=[basic_transport_belt, inserter],
    craft_time=6,
    machine_type={MT.Assembly},
    count=1,
    name='Automation Science Pack',
)
red_science = automation_science_pack

battery = Recipe(
    ingredients=[('sulfuric_acid', 20), ('plastic_bar', 1),
                 ('lead_plate', 2)],
    craft_time=4,
    machine_type={MT.ChemicalPlant},
    count=1,
    name='Battery',
)

accumulator = Recipe(
    ingredients=[('iron_plate', 2), (battery, 5)],
    craft_time=10,
    machine_type={MT.Assembly},
    count=1,
    name='Accumulator',
)
#######

Machine = namedtuple('Machine',
                     'machine_type,craft_speed,name')

ass1 = Machine(
    machine_type=MT.Assembly,
    craft_speed=0.5,
    name='Assembling Machine 1',
)

ass2 = Machine(
    machine_type=MT.Assembly,
    craft_speed=0.75,
    name='Assembling Machine 2',
)

elec1 = Machine(
    machine_type=MT.Electronics,
    craft_speed=1,
    name='Electronics Assembling Machine 1',
)

mm1 = Machine(
    machine_type=MT.MetalMixing,
    craft_speed=1,
    name='Stone Metal Mixing Furnace',
)

cf1 = Machine(
    machine_type=MT.ChemicalFurnace,
    craft_speed=1,
    name='Stone Chemical Furnace',
)

cp1 = Machine(
    machine_type=MT.ChemicalPlant,
    craft_speed=1,
    name='Chemical Plant',
)


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
