# Built-ins
import logging
import operator

# Third-party
from unstdlib.standard import listify

logger = logging.getLogger(__name__)

CLASSES = ["Witch", "Shadow", "Ranger", "Duelist", "Marauder", "Templar", "Scion"]


def evaluate_skill_gem(gem_name, class_, character, missing, quest_data, skill_data):
    # Vendor recipe skill gems
    if gem_name == "Mirror Arrow":
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
        base_gem_name = find_corresponding_non_vaal_skill_gem(gem_name)
        character.append(
            (
                gem_name,
                "Drop-only",
                int(skill_data[base_gem_name]["lvl"]),
                skill_data[base_gem_name]["colour"],
            )
        )
        gem_name = base_gem_name  # Rename to allow the base gem to be added as well
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
    dct = {
        "Vaal Breach": "Portal",
        "Vaal Impurity of Ice": "Purity of Ice",
        "Vaal Impurity of Fire": "Purity of Fire",
        "Vaal Impurity of Lightning": "Purity of Lightning",
        "Vaal Summon Skeletons": "Summon Skeletons",
    }
    return dct.get(skill_gem_name, skill_gem_name.partition("Vaal ")[2])


def find_skill_gems(skill_gems, class_, quest_data, skill_data):
    class_skill_gems = []
    for name in skill_gems:
        evaluate_skill_gem(name, class_, class_skill_gems, [], quest_data, skill_data)
    return class_, class_skill_gems


def sort_by_quest(tpl):
    class_, character_values = tpl
    character_values.sort(key=operator.itemgetter(2, 1, 0))
    return class_, character_values


@listify
def parse(build, quest_data, skill_data):
    class_ = build.class_name
    class_skill_gems = []
    missing_skill_gems = []
    for skill_gem in build.skill_gems:
        evaluate_skill_gem(
            skill_gem.name,
            class_,
            class_skill_gems,
            missing_skill_gems,
            quest_data,
            skill_data,
        )
    class_skill_gems = (class_, class_skill_gems)
    yield sort_by_quest(class_skill_gems)
    other_classes = [i for i in CLASSES if i != class_]
    other_class_skill_gems = [
        find_skill_gems(missing_skill_gems, class_, quest_data, skill_data)
        for class_ in other_classes
    ]
    # Sort by number of skill gems available to class
    other_class_skill_gems.sort(key=lambda x: len(x[1]))
    for other in other_class_skill_gems:
        yield sort_by_quest(other)
