import yaml
import xlsxwriter
# import numpy as np
# import json

from any_yaml import Loader
from pathlib import Path
# from chardet import UniversalDetector
# from PIL import Image, ImageColor
# from PIL.PngImagePlugin import PngInfo

from project_dirs import *
from locales import *
from rw_func import *
from glasses import *
from data import *


# Search for reagent sprites/anim and save them
# for reagents in reag_files:
#     check_and_reencode_utf_sig(reagents)

#     with open(reagents) as file:
#         data = yaml.load(file, Loader=Loader)

#     for i in range(len(data)):
#         print("[INFO] Loading sprites for " + str(Path(reagents).stem), i, data[i]["id"])

#         if ("metamorphicSprite" in data[i]) and ("sprite" in data[i]["metamorphicSprite"]):
#             metamorph_glass_file = PROJ_DIR.joinpath("Resources/Textures/"+data[i]["metamorphicSprite"]["sprite"]+"/icon.png")

#             with Image.open(metamorph_glass_file) as metamorph_glass:
#                 if get_metadata(metamorph_glass_file.with_name("meta.json"), mode="ifanim"):
#                     save_anim(metamorph_glass,
#                               metamorph_glass_file.parent.stem,
#                               *get_metadata(metamorph_glass_file.with_name("meta.json"), mode="anim"),
#                               *get_metadata(metamorph_glass_file.with_name("meta.json"), mode="copyright")
#                               )
#                 else:
#                     save_sprite(metamorph_glass,
#                                 metamorph_glass_file.parent.stem,
#                                 *get_metadata(metamorph_glass_file.with_name("meta.json")),
#                                 "Metamorphic"
#                                 )

#         if "id" in data[i] and "color" in data[i]:
#             for glass_type in glasses:
#                 glass_type.get_sprite(data[i]["id"], data[i]["color"])
#         else:
#             continue

with xlsxwriter.Workbook(SAVE_DIR.joinpath("TEMP.xlsx")) as xls_file:
    xls_worksheets = {reag_group: xls_file.add_worksheet(reag_group) for reag_group in reag_groups}
    order = {reag_group: 1 for reag_group in reag_groups} # Order counter for each group
    headers = {"ID": {"width": 12},
                "Цвет": {"width": 8},
                "Название en/ru": {"width": 15},
                "Описание en/ru": {"width": 30},
                "Физ. описание en/ru": {"width": 20},
                "Метаморф-спрайт": {"width": 8},
                "Анимированный спрайт": {"width": 8},
                "Рецепт": {"width": 16,
                           "format": xls_file.add_format({"align": "left",
                                                          "valign": "top"
                                                          })
                           }
                }

    main_row_format = xls_file.add_format({"bold": True,
                                      "align": "center",
                                      "valign": "vcenter",
                                      "text_wrap": True,
                                      "bg_color": "#BFBFBF",
                                      "bottom": 6})

    blue_format = {"main": xls_file.add_format({"bg_color": "#95B3D7"}),
                   "first": xls_file.add_format({"bg_color": "#DCE6F1"}),
                   "second": xls_file.add_format({"bg_color": "#B8CCE4"})
                   }
    red_format = {"main": xls_file.add_format({"bg_color": "#DA9694"}),
                  "first": xls_file.add_format({"bg_color": "#F2DCDB"}),
                  "second": xls_file.add_format({"bg_color": "#E6B8B7"})
                  }

    for worksheet in xls_worksheets.values():
        worksheet.write_row(0, 0, headers.keys(), main_row_format)
        k = 0
        for col in headers.values():
            if "format" in col:
                worksheet.set_column(k, k, col["width"], col["format"])
            else:
                worksheet.set_column(k, k, col["width"])
            k += 1

    for reagent, properties in reagents.items():
        animation, main_sprite = None, None
        print("[INFO] Writing: "+str(reagent))

        # Search for membership group
        if "group" in properties:
            group = properties["group"]
        # Search for parent membership group
        elif "parent" in properties:
            parent_reagent = reagents[reagent]
            while not("group" in parent_reagent):
                if not("parent" in parent_reagent):
                    print(f"[WARN] The {reagent} has no group.")
                    group = "reagent"
                    break
                parent_reagent = reagents[parent_reagent["parent"]]
            group = parent_reagent["group"]
        else:
            print(f"[WARN] The {reagent} has no group.")
            group = "reagent"

        if (order[group]+1) % 4:
            color_format = blue_format
        else:
            color_format = red_format

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


        xls_worksheets[group].set_default_row(21.25)
        xls_worksheets[group].set_row(order[group], None, color_format["first"])
        xls_worksheets[group].set_row(order[group]+1, None, color_format["second"])

        xls_worksheets[group].merge_range(order[group], 0, order[group]+1, 0, "")
        xls_worksheets[group].write(order[group], 0, reagent, color_format["main"])

        if "name" in properties:
            xls_worksheets[group].write(order[group], 2, get_locale("en", properties["name"]))
            xls_worksheets[group].write(order[group]+1, 2, get_locale("ru", properties["name"]))

        if "desc" in properties:
            xls_worksheets[group].write(order[group], 3, get_locale("en", properties["desc"]))
            xls_worksheets[group].write(order[group]+1, 3, get_locale("ru", properties["desc"]))

        if "physicalDesc" in properties:
            xls_worksheets[group].write(order[group], 4, get_locale("en", properties["physicalDesc"]))
            xls_worksheets[group].write(order[group]+1, 4, get_locale("ru", properties["physicalDesc"]))

        if main_sprite:
            xls_worksheets[group].merge_range(order[group], 5, order[group]+1, 5, "")
            xls_worksheets[group].insert_image(order[group], 5, main_sprite, {'x_scale': 0.23, 'y_scale': 0.23})

        if animation:
            xls_worksheets[group].merge_range(order[group], 6, order[group]+1, 6, "")
            xls_worksheets[group].insert_image(order[group], 6, animation, {'x_scale': 0.23, 'y_scale': 0.23})

        if reagent in recipes and recipes[reagent] != {}:
            recipe = ""
            for reactant, amount in recipes[reagent].items():
                recipe += f"{reactant}: {amount}\r\n"
            xls_worksheets[group].merge_range(order[group], 7, order[group]+1, 7, "")
            xls_worksheets[group].write(order[group], 7, recipe)

        if "color" in properties:
            xls_worksheets[group].merge_range(order[group], 1, order[group]+1, 1, "")
            xls_worksheets[group].write(order[group], 1, properties["color"])

            n = 8
            for glass_type in glasses:
                sprite = glass_type.get_sprite(reagent, properties["color"])
                xls_worksheets[group].merge_range(order[group], n, order[group]+1, n, "")
                xls_worksheets[group].insert_image(order[group], n, sprite, {'x_scale': 0.23, 'y_scale': 0.23})

                n += 1

        order[group] += 2


    # for reac_file in reac_files:
    #     xls_worksheet = xls_file.add_worksheet(str(Path(reac_file).stem))
    #     check_and_reencode_utf_sig(reac_file)

    #     with open(reac_file) as file:
    #         data = yaml.load(file, Loader=Loader)

    #     for i in range(len(data)):
    #         print("Writing: "+str(Path(reac_file).stem), i, data[i]["id"])
    #         match data[i]:
    #             case "type": xls_worksheet.write(i, 0, str(data[i]["type"]))
    #             case "id": xls_worksheet.write(i, 1, str(data[i]["id"]))
    #             case "reactants": xls_worksheet.write(i, 2, str(data[i]["reactants"]))
    #             case "products": xls_worksheet.write(i, 3, str(data[i]["products"]))

