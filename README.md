# Quickstart

Download:

```shell_script
git clone https://github.com/craymichael/Factorio-Recipe-Balancer.git
cd Factorio-Recipe-Balancer
```

Running: example below shows balanced recipe to produce 2 advanced circuits per second. Recipes
for plates are suppressed in the output with the option `--ignore-basic`. Note that the data file
in this repository assumes Bob's mods, Factorissimo, and a handful of other mods with minor side
effects or new recipes.

```shell_script
./ratios.py --recipe advanced-circuit --rate 2 --ignore-basic
```

For all options:

```shell_script
$ ./ratios.py --help
usage: ratios.py [-h] [--rate RATE] --recipe RECIPE [--ignore IGNORE [IGNORE ...]] [--ignore-basic]

Factorio recipe calculator

optional arguments:
  -h, --help            show this help message and exit
  --rate RATE, -r RATE  rate of production of target recipe (default: 1)
  --recipe RECIPE, -R RECIPE
                        the recipe to make (default: None)
  --ignore IGNORE [IGNORE ...], -i IGNORE [IGNORE ...]
                        do not show ingredients for these recipes (default: [])
  --ignore-basic, -I    ignore basic items you have on your bus, probably (default: False)
```

# Using other recipes
If the data file for other recipes is not in the `data/` folder here, you can open a game, hit the
`` ` `` key, then paste the contents of the `extract_recipes.lua` script and run it. The game will save
a file called `recipes.json` to your game directory `~/.factorio/script-output` on Linux and somewhere
in `%APPDATA%\Factorio` or whatever it ends up being on Windows. The script should be able to handle
recipes that does not require new machines beyond what it already knows about...

Kudos to [this repo](https://github.com/antropod/factorio) for the script!
