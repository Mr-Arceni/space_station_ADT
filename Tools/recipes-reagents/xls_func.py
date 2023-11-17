from project_dirs import *
from data import *
from locales import *
from glasses import *


def get_xls_format(xls_format, xls_file, mode="single") -> any:
    match mode:
        case "single":
            return xls_file.add_format(xls_format)
        case "multi":
            return {key: xls_file.add_format(xls_format_prop) for key, xls_format_prop in xls_format.items()}


def xls_write_reagent(reagent, properties: dict, order: dict, xls_worksheets, first_format=None, second_format=None) -> None:
    animation, main_sprite = None, None
    print("[INFO] Writing: "+str(reagent))

    # Search and add parent reagent properties
    if "parent" in properties:
        parent_properties = [properties.copy()]
        while "parent" in parent_properties[-1]:
            parent_properties.append(reagents[parent_properties[-1]["parent"]])
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
        xls_worksheets[group].merge_range(order[group], col, order[group]+1, 1, "")
        xls_worksheets[group].write(order[group], col, properties["color"])

    col += 1
    if "name" in properties:
        xls_worksheets[group].write(order[group], col, get_locale("en", properties["name"]))
        xls_worksheets[group].write(order[group]+1, col, get_locale("ru", properties["name"]))

    col += 1
    if "desc" in properties:
        xls_worksheets[group].write(order[group], col, get_locale("en", properties["desc"]))
        xls_worksheets[group].write(order[group]+1, col, get_locale("ru", properties["desc"]))

    col += 1
    if "physicalDesc" in properties:
        xls_worksheets[group].write(order[group], col, get_locale("en", properties["physicalDesc"]))
        xls_worksheets[group].write(order[group]+1, col, get_locale("ru", properties["physicalDesc"]))

    col += 1
    if main_sprite:
        xls_worksheets[group].merge_range(order[group], col, order[group]+1, 5, "")
        xls_worksheets[group].insert_image(order[group], col, main_sprite, {'x_scale': 0.23, 'y_scale': 0.23})

    col += 1
    if animation:
        xls_worksheets[group].merge_range(order[group], col, order[group]+1, 6, "")
        xls_worksheets[group].insert_image(order[group], col, animation, {'x_scale': 0.23, 'y_scale': 0.23})

    col += 1
    if reagent in recipes and recipes[reagent] != {}:
        recipe = ""
        for reactant, amount in recipes[reagent].items():
            recipe += f"{reactant}: {amount}\r\n"
        xls_worksheets[group].merge_range(order[group], col, order[group]+1, 7, "")
        xls_worksheets[group].write(order[group], col, recipe)

    col += 1
    if "color" in properties:
        for glass_type in glasses:
            sprite = glass_type.get_sprite(reagent, properties["color"])
            xls_worksheets[group].merge_range(order[group], col, order[group]+1, col, "")
            xls_worksheets[group].insert_image(order[group], col, sprite, {'x_scale': 0.23, 'y_scale': 0.23})
            col += 1

    order[group] += 2
