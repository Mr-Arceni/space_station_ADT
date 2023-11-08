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


reac_files = sorted(RECP_DIR.joinpath("Reactions").glob("**/*.yml"))
reag_files = sorted(REAG_DIR.glob("**/*.yml"))

# Search for reagent sprites/anim and save them
for reagents in reag_files:
    check_and_reencode_utf_sig(reagents)

    with open(reagents) as file:
        data = yaml.load(file, Loader=Loader)

    for i in range(len(data)):
        print("[INFO] Loading sprites for " + str(Path(reagents).stem), i, data[i]["id"])

        if ("metamorphicSprite" in data[i]) and ("sprite" in data[i]["metamorphicSprite"]):
            metamorph_glass_file = PROJ_DIR.joinpath("Resources/Textures/"+data[i]["metamorphicSprite"]["sprite"]+"/icon.png")

            with Image.open(metamorph_glass_file) as metamorph_glass:
                if get_metadata(metamorph_glass_file.with_name("meta.json"), mode="ifanim"):
                    save_anim(metamorph_glass,
                              metamorph_glass_file.parent.stem,
                              *get_metadata(metamorph_glass_file.with_name("meta.json"), mode="anim"),
                              *get_metadata(metamorph_glass_file.with_name("meta.json"), mode="copyright")
                              )
                else:
                    save_sprite(metamorph_glass,
                                metamorph_glass_file.parent.stem,
                                *get_metadata(metamorph_glass_file.with_name("meta.json")),
                                "Metamorphic"
                                )

        if "id" in data[i] and "color" in data[i]:
            for glass_type in glasses:
                glass_type.get_sprite(data[i]["id"], data[i]["color"])
        else:
            continue

with xlsxwriter.Workbook(SAVE_DIR.joinpath('TEMP.xlsx')) as xls_file:

    for reag_file in reag_files:
        xls_worksheet = xls_file.add_worksheet(str(Path(reag_file).stem))
        check_and_reencode_utf_sig(reag_file)

        with open(reag_file) as file:
            data = yaml.load(file, Loader=Loader)

        for i in range(len(data)):
            print("[INFO] Writing: "+str(Path(reag_file).stem), i, data[i]["id"])

            xls_worksheet.write(i, 2, str(data[i]["id"]))
            if "reactants" in data[i]:
                xls_worksheet.write(i, 3, str(data[i]["reactants"]))
            if "products" in data[i]:
                xls_worksheet.write(i, 4, str(data[i]["products"]))




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

