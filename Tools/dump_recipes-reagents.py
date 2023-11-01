import yaml
import xlsxwriter
import numpy as np
import json

from any_yaml import Loader
from pathlib import Path
from chardet import UniversalDetector
from PIL import Image, ImageColor
from PIL.PngImagePlugin import PngInfo

# Checking the working directory and declaring path constants in the project
if not(Path(__file__).parents[1].joinpath("Resources/Prototypes/Recipes").exists()) or not(Path(__file__).parents[1].joinpath("Resources/Prototypes/Reagents").exists()):
    print("'../Resources/Prototypes/Recipes' or '../Resources/Prototypes/Reagents' were not found. \nSpecify the absolute path to the project, or move this file to [PROJECT_DIR]/Tools \n\nEnter [0] to exit")
    entered_path = input()

    while not(Path(entered_path).is_dir()) or not(Path(entered_path).joinpath("Resources/Prototypes/Recipes").exists()) or not(Path(entered_path).joinpath("Resources/Prototypes/Reagents").exists()):
        if entered_path == "0": exit()
        print("Entered path is not a dir, or does not exist, or not specified to SS14 project dir \nTry again")
        entered_path = input()

    PROJ_DIR = Path(entered_path)

else:
    PROJ_DIR = Path(__file__).parents[1]

RECP_DIR = PROJ_DIR.joinpath("Resources/Prototypes/Recipes")
REAG_DIR = PROJ_DIR.joinpath("Resources/Prototypes/Reagents")
SAVE_DIR = PROJ_DIR.joinpath("Tools/recipes-reagents")
SRTE_DIR = SAVE_DIR.joinpath("sprites")

if not(SRTE_DIR.joinpath("animations").exists()):
    SRTE_DIR.joinpath("animations").mkdir(parents=True)

# Constructor for reagent containers sprites
class SpriteOfLiquidContainer:

    def __init__(self, glass_name, fill, back_sprite=None, front_sprite=None, image_copyright=None, image_license=None):
        self.glass_name = glass_name
        self.fill = fill
        self.back_sprite = back_sprite
        self.front_sprite = front_sprite
        self.image_copyright = image_copyright
        self.image_license = image_license

        if self.fill.with_name("meta.json").exists():
            image_file_copyright, image_file_license = get_metadata(self.fill.with_name("meta.json"))

        if not(back_sprite) and not(front_sprite):
            raise ValueError(f"The 'back_sprite' and 'front_sprite' is not defined in object {self.glass_name}. You have to define at least one.")

        if not(image_file_license) or not(image_file_copyright):
            print(f"meta.json has no license or/and copyright in {self.glass_name}")

        elif self.image_license or self.image_copyright:
            print("meta.json has license and copyright, but there have been defined image_license or/and image_copyright.\nDefined values will be used INSTEAD values from meta.json")

        if not(self.image_license):
            self.image_license = image_file_license
        if not(self.image_copyright):
            self.image_copyright = image_file_copyright

        if (not(image_file_license) and not(self.image_license)) or (not(image_file_copyright) and not(self.image_copyright)):
            print(f"The copyright or license of {self.glass_name} is not defined or not found in meta.json")
            self.image_copyright = f"From the {Path(PROJ_DIR.name)}"
            self.image_license = "UNKNOWN LICENSE"


    def get_sprite(self, name, color=None):
        if not(color):
            print(f"There is no liquid color for {name}. Skip")
            return None

        r, g, b, a = ImageColor.getcolor(color, "RGBA") # type: ignore

        # Assembling the sprite
        with Image.open(self.fill) as fill:
            fill = fill.convert("RGBA")
            fill_raw = np.array(fill)
            fill_raw = fill_raw / 255 * [r, g, b, a]
            liqd = Image.fromarray(fill_raw.astype(np.uint8))

        if self.back_sprite and self.front_sprite:
            with (
                Image.open(self.back_sprite) as back,
                Image.open(self.front_sprite) as front
            ):
                sprite = Image.alpha_composite(Image.alpha_composite(back, liqd), front)

        elif self.back_sprite:
            with Image.open(self.back_sprite) as back:
                sprite = Image.alpha_composite(back, liqd)

        elif self.front_sprite:
            with Image.open(self.front_sprite) as front:
                sprite = Image.alpha_composite(liqd, front)

        else:
            return None

        return save_sprite(sprite, name, self.image_copyright, self.image_license, self.glass_name)


# Files with BOM cause a yaml.scanner.scannererror and json.decoder.JSONDecodeError exceptions
# That function check if file have BOM, remove them and rewrite it
def check_and_reencode_utf_sig(file):
    u = UniversalDetector()
    u.reset()

    with open(file, 'rb') as bfile:
        for line in bfile:
            u.feed(line)
            if u.done: break
    u.close()

    if u.result["encoding"] == "UTF-8-SIG":
        print(f"Found UTF-8-SIG in {file} \nChange encoding to UTF-8 (remove BOM)")
        content_sig_file = Path(file).read_text(encoding="UTF-8-SIG")
        new_file = Path(file).with_suffix(".tmp")
        new_file.touch()

        Path(new_file).write_text(content_sig_file, encoding="UTF-8")
        Path(new_file).replace(file)
        print("Encoding changed successfully")

def get_metadata(file, mode=None):
    check_and_reencode_utf_sig(file)

    with open(file, "r") as metadata_content:
        data = json.loads(metadata_content.read())

    delays = None
    for key, value in data.items():
        if key == "copyright": copyright_data = value
        if key == "license": license_data = value
        if key == "size": M, N = value["x"], value["y"]
        if key == "states" and "delays" in value[0]: delays = value[0]["delays"]

    match mode:
        case "copyright":
            return copyright_data, license_data
        case "anim":
            return M, N, delays
        case "ifanim":
            return True if delays else False
        case _:
            return copyright_data, license_data

def save_sprite(sprite, name, image_copyright, image_license, glass_name=None):
    metadata = PngInfo()
    metadata.add_text("Copyright", f"{glass_name or ''}{name}\n{image_copyright} Is licensed under {image_license}") # type: ignore

    sprite = sprite.resize((256, 256), Image.NEAREST)
    sprite.save(SRTE_DIR.joinpath(f"{name}_{glass_name or 'Metamorphic'}.png"), pnginfo=metadata)
    return SRTE_DIR.joinpath(f"{name}_{glass_name or 'Metamorphic'}.png")

def save_anim(sprite, name, M, N, delays, image_copyright, image_license):
    raw_img = np.array(sprite)

    tiles = [
        raw_img[x:x+M,y:y+N]
        for x in range(0, raw_img.shape[0], M)
        for y in range(0, raw_img.shape[1], N)
        ]

    frames = []
    for i in range(len(tiles)-1):
        frame = Image.fromarray(tiles[i]).resize((256, 256), Image.NEAREST)
        frames.append(frame)

    metadata_text = f"{name}\n{image_copyright} Is licensed under {image_license}"
    frames[0].save(SRTE_DIR.joinpath("animations", f"{name}.gif"),
                format='GIF',
                optimize=True,
                append_images=frames[1:len(delays[0])],
                disposal=2,
                save_all=True,
                duration=delays[0],
                loop=0,
                comment=metadata_text)
    return SRTE_DIR.joinpath("animations", f"{name}.gif")


# Create containers for liquid
beaker = SpriteOfLiquidContainer(
    glass_name="beaker",
    back_sprite=PROJ_DIR.joinpath("Resources/Textures/Objects/Specific/Chemistry/beaker.rsi/beaker.png"),
    fill=PROJ_DIR.joinpath("Resources/Textures/Objects/Specific/Chemistry/beaker.rsi/beaker6.png")
)
beakerlarge = SpriteOfLiquidContainer(
    glass_name="beakerlarge",
    back_sprite=PROJ_DIR.joinpath("Resources/Textures/Objects/Specific/Chemistry/beaker_large.rsi/beakerlarge.png"),
    fill=PROJ_DIR.joinpath("Resources/Textures/Objects/Specific/Chemistry/beaker_large.rsi/beakerlarge6.png")
)
glass = SpriteOfLiquidContainer(
    glass_name="glass",
    back_sprite=PROJ_DIR.joinpath("Resources/Textures/Objects/Consumable/Drinks/glass_clear.rsi/icon.png"),
    front_sprite=PROJ_DIR.joinpath("Resources/Textures/Objects/Consumable/Drinks/glass_clear.rsi/icon-front.png"),
    fill=PROJ_DIR.joinpath("Resources/Textures/Objects/Consumable/Drinks/glass_clear.rsi/fill9.png")
)
glass_coupe_shape = SpriteOfLiquidContainer(
    glass_name="glass_coupe_shape",
    back_sprite=PROJ_DIR.joinpath("Resources/Textures/Objects/Consumable/Drinks/glass_coupe_shape.rsi/icon.png"),
    front_sprite=PROJ_DIR.joinpath("Resources/Textures/Objects/Consumable/Drinks/glass_coupe_shape.rsi/icon-front.png"),
    fill=PROJ_DIR.joinpath("Resources/Textures/Objects/Consumable/Drinks/glass_coupe_shape.rsi/fill5.png")
)
jug = SpriteOfLiquidContainer(
    glass_name="jug",
    back_sprite=PROJ_DIR.joinpath("Resources/Textures/ADT/Objects/Misc/glass_jug.rsi/icon.png"),
    front_sprite=PROJ_DIR.joinpath("Resources/Textures/ADT/Objects/Misc/glass_jug.rsi/icon-front.png"),
    fill=PROJ_DIR.joinpath("Resources/Textures/ADT/Objects/Misc/glass_jug.rsi/fill6.png")
)

glasses = [beaker, beakerlarge, glass, glass_coupe_shape, jug]
reac_files = sorted(RECP_DIR.joinpath("Reactions").glob("*.yml"))
drinks = sorted(REAG_DIR.joinpath("Consumable/Drink").glob("*.yml"))


for drink in drinks:
    check_and_reencode_utf_sig(drink)

    with open(drink) as file:
        data = yaml.load(file, Loader=Loader)

    for i in range(len(data)):
        print(str(Path(drink).stem), i, data[i]["id"])

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
                                *get_metadata(metamorph_glass_file.with_name("meta.json"))
                                )

        if "id" in data[i] and "color" in data[i]:
            name = data[i]["id"]
            color = data[i]["color"]
        else:
            continue

        for glass_type in glasses:
            glass_type.get_sprite(name, color)

with xlsxwriter.Workbook('TEMP.xlsx') as xls_file:
    for reac_file in reac_files:
        xls_worksheet = xls_file.add_worksheet(str(Path(reac_file).stem))
        check_and_reencode_utf_sig(reac_file)

        with open(reac_file) as file:
            data = yaml.load(file, Loader=Loader)

        for i in range(len(data)):
            print(str(Path(reac_file).stem), i, data[i]["id"]) #DEBUG PRINT
            if "type" in data[i]: xls_worksheet.write(i, 0, str(data[i]["type"]))
            if "id" in data[i]: xls_worksheet.write(i, 1, str(data[i]["id"]))
            if "reactants" in data[i]: xls_worksheet.write(i, 2, str(data[i]["reactants"]))
            if "products" in data[i]: xls_worksheet.write(i, 3, str(data[i]["products"]))

