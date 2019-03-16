# Built-ins
import json
import operator

# Third-party
from unstdlib.standard import listify

CLASSES = ["Witch", "Shadow", "Ranger", "Duelist", "Marauder", "Templar", "Scion"]


def sort_by_values_len(dct):
    dict_len = {key: len(value) for key, value in dct.items()}
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dct[item[0]]} for item in sorted_key_list]
    return sorted_dict


def evaluate_skill_gem(gem_name, class_, character, missing):
    with open("quest_data.json", "r") as f:
        quest_data = json.load(f)
    with open("skill_data.json", "r") as f:
        skill_data = json.load(f)

    # Gems available from Lily
    # TODO: Move gems to quest data
    if gem_name == "Added Chaos Damage":
        character.append((gem_name, "Fallen from Grace", 31, "blue"))
        return
    elif gem_name == "Detonate Mines":
        character.append((gem_name, "Fallen from Grace", 8, "white"))
        return
    # Drop-only skill gems
    elif gem_name == "Empower":
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
    # TODO: Vendor recipe skill gems
    elif gem_name == "Mirror Arrow":
        "Blink Arrow + 1 Orb of Alteration"
        pass
    elif gem_name == "Block Chance Reduction":
        "Puncture + any dexterity shield with 20% quality"
        pass
    # TODO: Why are the names of source skills empty?
    # elif gem_name == "":
    #     return
    # TODO: Vaal Skills
    # Portal corruption -> Vaal Breach
    elif gem_name == "Vaal Breach":
        character.append((gem_name, "Drop-only", 10, "white"))
        return
    elif gem_name == "Vaal Summon Skeletons":
        gem_name = "Summon Skeleton"
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
    try:
        missing.append(gem_name)
    except:
        pass


def find_skill_gems(skill_gems, class_):
    character = []
    for name in skill_gems:
        evaluate_skill_gem(name, class_, character, [])
    return character


def sort_by_level_quest_name(ch):
    cls = list(ch.keys())[0]
    cv = list(ch.values())[0]
    cv.sort(key=operator.itemgetter(2, 1, 0))
    cv = {cls: cv}
    return cv


@listify
def parse(build):
    class_ = build.class_name
    character = []
    missing = []
    for gem in build.skill_gems:
        evaluate_skill_gem(gem.name, class_, character, missing)
    other_classes = [c for c in CLASSES if c != class_]
    # other_classes.remove(class_)
    # print(missing)
    dump = {cls: find_skill_gems(missing, cls) for cls in other_classes}
    character = {class_: character}
    # print(character, missing)
    cv = sort_by_level_quest_name(character)
    yield cv
    dump = sort_by_values_len(dump)
    for d in dump:
        yield sort_by_level_quest_name(d)
