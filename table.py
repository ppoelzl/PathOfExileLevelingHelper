# Built-ins
from dataclasses import dataclass

# Third-party
from flask_table import Table, Col


class ItemTable(Table):
    gem_name = Col('Gem')
    quest_name = Col('Quest')
    gem_level = Col("Level")
    gem_colour = Col("Colour")


@dataclass
class Item:
    gem_name: str
    quest_name: str
    gem_level: int
    gem_colour: str


def generate_table(store):
    for cls in store:
        for cc, gems in cls.items():
            yield (cc, ItemTable([Item(*g) for g in gems], border=True))
