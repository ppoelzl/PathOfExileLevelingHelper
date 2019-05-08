# Built-ins
import json
import logging
import operator

# Third-party
from unstdlib.standard import listify

logger = logging.getLogger(__name__)

CLASSES = ["Witch", "Shadow", "Ranger", "Duelist", "Marauder", "Templar", "Scion"]

with open("quest_data.json", "r") as f:
    quest_data = json.load(f)
with open("skill_data.json", "r") as f:
    skill_data = json.load(f)


def sort_by_values_len(dct):
    tuple_list = [(key, len(value)) for key, value in dct.items()]
    sorted_tuple_list = sorted(tuple_list, key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dct[item[0]]} for item in sorted_tuple_list]
    return sorted_dict


def evaluate_skill_gem(gem_name, class_, character, missing):
    # Drop-only skill gems
    if gem_name == "Empower":
        character.append((gem_name, "Drop-only", 1, "red"))
        return
    elif gem_name == "Enhance":
        character.append((gem_name, "Drop-only", 1, "green"))
        return
    elif gem_name == "Enlighten":
        character.append((gem_name, "Drop-only", 1, "blue"))
        return
    elif gem_name == "Portal":
        character.append((gem_name, "Drop-only", 10, "white"))
        return
    # Vendor recipe skill gems
    elif gem_name == "Mirror Arrow":
        character.append(
            (
                gem_name,
                "Vendor Blink Arrow + 1 Orb of Alteration",
                int(skill_data[gem_name]["lvl"]),
                skill_data[gem_name]["colour"],
            )
        )
        return
    elif gem_name == "Block Chance Reduction":
        character.append(
            (
                gem_name,
                "Vendor Puncture + any dexterity based shield with 20% quality",
                int(skill_data[gem_name]["lvl"]),
                skill_data[gem_name]["colour"],
            )
        )
        return
    # Vaal Skills
    if gem_name.startswith("Vaal"):
        vaal_gem_name = gem_name
        gem_name = find_corresponding_non_vaal_skill_gem(gem_name)
        character.append(
            (
                vaal_gem_name,
                "Drop-only",
                int(skill_data[gem_name]["lvl"]),
                skill_data[gem_name]["colour"],
            )
        )
    # TODO: Why are the names of source skills empty?
    try:
        for quest in quest_data:
            if gem_name in quest_data[quest][class_]:
                character.append(
                    (
                        gem_name,
                        quest,
                        int(skill_data[gem_name]["lvl"]),
                        skill_data[gem_name]["colour"],
                    )
                )
                return
        missing.append(gem_name)
    except KeyError:
        logger.debug(f"{gem_name} is missing from skill data.")


def find_corresponding_non_vaal_skill_gem(skill_gem_name):
    if skill_gem_name == "Vaal Breach":
        name = "Portal"
    elif skill_gem_name == "Vaal Impurity of Ice":
        name = "Purity of Ice"
    elif skill_gem_name == "Vaal Impurity of Fire":
        name = "Purity of Fire"
    elif skill_gem_name == "Vaal Impurity of Lightning":
        name = "Purity of Lightning"
    elif skill_gem_name == "Vaal Summon Skeletons":
        name = "Summon Skeletons"
    else:
        _, _, name = skill_gem_name.partition("Vaal ")
    return name


def find_skill_gems(skill_gems, class_):
    character = []
    for name in skill_gems:
        evaluate_skill_gem(name, class_, character, [])
    return character


def sort_by_quest(character_class):
    class_ = list(character_class.keys())[0]
    character_values = list(character_class.values())[0]
    character_values.sort(key=operator.itemgetter(2, 1, 0))
    character_values = {class_: character_values}
    return character_values


@listify
def parse(build):
    class_ = build.class_name
    class_skill_gems = []
    missing_skill_gems = []
    for skill_gem in build.skill_gems:
        evaluate_skill_gem(skill_gem.name, class_, class_skill_gems, missing_skill_gems)
    class_skill_gems = {class_: class_skill_gems}
    yield sort_by_quest(class_skill_gems)
    other_classes = [i for i in CLASSES if i != class_]
    other_skill_gems = {
        class_: find_skill_gems(missing_skill_gems, class_) for class_ in other_classes
    }
    other_skill_gems = sort_by_values_len(other_skill_gems)
    for other in other_skill_gems:
        yield sort_by_quest(other)
