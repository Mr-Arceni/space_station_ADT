from project_dirs import *
from data import *
from locales import *
from glasses import *

if __name__ == "__main__":
    print("[ERR] Run the RUN.py")
    exit()

def parsing_reagent_effects(reagent: dict) -> str:
    str_reagent_effects = ""

    for metabolism in reagent["metabolisms"].keys():
        str_reagent_effects += (f"\r\nМетаболизатор: {metabolism}")

        reagent_effects = reagent["metabolisms"][metabolism]["effects"]
        for effect in reagent_effects.keys():
            try:
                reagent_effect = effects[effect].copy()
            except KeyError:
                print(f"[ERR] `effects` does not have the {effect}.\nExit")
                exit()

            reagent_effect.update(reagent_effects[effect])
            names = reagent_effect["NAMES"]

            str_reagent_effects += (f"\r\n- {names['MAIN']}")
            for key, value in reagent_effect.items():
                if key == "NAMES": continue
                if key in names:
                    str_reagent_effects += (f"\r\n   - {names[key]}: {value}")
                else:
                    str_reagent_effects += (f"\r\n   - {key}: {value}")

    return str_reagent_effects

def get_xls_format(xls_format: dict, xls_file: object, mode: str = "single") -> object | dict:
    match mode:
        case "single":
            return xls_file.add_format(xls_format)
        case "multi":
            return {key: xls_file.add_format(xls_format_prop) for key, xls_format_prop in xls_format.items()}


def xls_write_reagent(reagent: str, properties: dict, order: dict, xls_worksheets: dict, first_format: object = None, second_format: object = None, true_format: dict = None, false_format: dict = None) -> None:
    animation, main_sprite = None, None
    print("[INFO] Writing: "+str(reagent))

    # Search and add parent reagent properties
    if "parent" in properties:
        parent_properties = [properties.copy()]
        while "parent" in parent_properties[-1]:
            parent_reagent = reagents[parent_properties[-1]["parent"]].copy()
            if "abstract" in parent_reagent:
                parent_reagent.pop("abstract")
            parent_properties.append(parent_reagent)
        parent_properties.reverse()

        properties.clear()
        for parent_property in parent_properties:
            properties.update(parent_property)

    # Search for membership group
    if "group" in properties:
        group = properties["group"]
    else:
        print(f"[WARN] The {reagent} has no group.")
        group = "reagent"

    if (order[group]+1) % 4:
        color_format = first_format
    else:
        color_format = second_format

    if ("metamorphicSprite" in properties) and ("sprite" in properties["metamorphicSprite"]):
        metamorph_glass_file = PROJ_DIR.joinpath("Resources/Textures/"+properties["metamorphicSprite"]["sprite"]+"/icon.png")

        with Image.open(metamorph_glass_file) as metamorph_glass:
            if get_metadata(metamorph_glass_file.with_name("meta.json"), mode="ifanim"):
                animation = save_anim(metamorph_glass,
                            metamorph_glass_file.parent.stem,
                            *get_metadata(metamorph_glass_file.with_name("meta.json"), mode="anim"),
                            *get_metadata(metamorph_glass_file.with_name("meta.json"), mode="copyright")
                            )
            else:
                main_sprite = save_sprite(metamorph_glass,
                            metamorph_glass_file.parent.stem,
                            *get_metadata(metamorph_glass_file.with_name("meta.json")),
                            "Metamorphic"
                            )

    col = 0

    xls_worksheets[group].set_default_row(21.25)
    xls_worksheets[group].set_row(order[group], None, color_format["first"])
    xls_worksheets[group].set_row(order[group]+1, None, color_format["second"])

    xls_worksheets[group].merge_range(order[group], col, order[group]+1, 0, "")
    xls_worksheets[group].write(order[group], col, reagent, color_format["main"])

    col += 1
    if "color" in properties:
        xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
        xls_worksheets[group].write(order[group], col, properties["color"])

    col += 1
    if "name" in properties:
        xls_worksheets[group].write(order[group], col, get_name("en", properties["name"]))
        xls_worksheets[group].write(order[group]+1, col, get_name("ru", properties["name"]))

    col += 1
    if "desc" in properties:
        xls_worksheets[group].write(order[group], col, get_name("en", properties["desc"]))
        xls_worksheets[group].write(order[group]+1, col, get_name("ru", properties["desc"]))

    col += 1
    if "physicalDesc" in properties:
        xls_worksheets[group].write(order[group], col, get_name("en", properties["physicalDesc"]))
        xls_worksheets[group].write(order[group]+1, col, get_name("ru", properties["physicalDesc"]))

    col += 1
    xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
    if main_sprite:
        xls_worksheets[group].insert_image(order[group], col, main_sprite, {'x_scale': 0.23, 'y_scale': 0.23})

    col += 1
    xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
    if animation:
        xls_worksheets[group].insert_image(order[group], col, animation, {'x_scale': 0.23, 'y_scale': 0.23})

    col += 1
    xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
    if reagent in recipes and recipes[reagent] != {}:
        recipe = ""
        for reactant, amount in recipes[reagent].items():
            recipe += f"{reactant}: {amount}\r\n"
        xls_worksheets[group].write(order[group], col, recipe)

    col += 1
    xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
    if "recognizable" in properties:
        if properties["recognizable"]:
            xls_worksheets[group].write(order[group], col, "Да", true_format)
        else:
            xls_worksheets[group].write(order[group], col, "Нет", false_format)
    else:
        xls_worksheets[group].write(order[group], col, "Нет", false_format)

    col += 1
    xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
    if "slippery" in properties:
        if properties["slippery"]:
            xls_worksheets[group].write(order[group], col, "Да", true_format)
        else:
            xls_worksheets[group].write(order[group], col, "Нет", false_format)
    else:
        xls_worksheets[group].write(order[group], col, "Нет", false_format)

    col += 1
    xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
    if "abstract" in properties:
        if properties["abstract"]:
            xls_worksheets[group].write(order[group], col, "Да", true_format)
        else:
            xls_worksheets[group].write(order[group], col, "Нет", false_format)
    else:
        xls_worksheets[group].write(order[group], col, "Нет", false_format)

    col += 1
    if "metabolisms" in properties:
        xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
        xls_worksheets[group].write(order[group], col, parsing_reagent_effects(properties))

    col += 1
    if "color" in properties:
        for glass_type in glasses:
            sprite = glass_type.get_sprite(reagent, properties["color"])
            xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
            xls_worksheets[group].insert_image(order[group], col, sprite, {'x_scale': 0.23, 'y_scale': 0.23})
            col += 1


    order[group] += 2
