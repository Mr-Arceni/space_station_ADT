import numpy as np
import json
import os

from pathlib import Path
from chardet import UniversalDetector
from PIL import Image, ImageColor
from PIL.PngImagePlugin import PngInfo

from project_dirs import *

if __name__ == "__main__":
    print("[ERR] Run the RUN.py")
    exit()


# Constructor for reagent containers sprites
class SpriteOfLiquidContainer:

    def __init__(self, glass_name: str, fill: str | os.PathLike, back_sprite: str | os.PathLike = None, front_sprite: str | os.PathLike = None, image_copyright: str = None, image_license: str = None):
        self.glass_name = glass_name
        self.fill = Path(fill)
        self.back_sprite = Path(back_sprite) if back_sprite else None
        self.front_sprite = Path(front_sprite) if front_sprite else None
        self.image_copyright = image_copyright
        self.image_license = image_license

        if not(back_sprite) and not(front_sprite):
            raise ValueError(f"The 'back_sprite' and 'front_sprite' is not defined in object {self.glass_name}. You have to define at least one.")

        if self.fill.with_name("meta.json").exists():
            image_file_copyright, image_file_license = get_metadata(self.fill.with_name("meta.json"))

        if not(image_file_license) or not(image_file_copyright):
            print(f"[WARN] meta.json has no license or/and copyright in {self.glass_name}")
        elif self.image_license or self.image_copyright:
            print("[WARN] meta.json has license and copyright, but there have been defined image_license or/and image_copyright.\nDefined values will be used INSTEAD values from meta.json")

        if not(self.image_license):
            self.image_license = image_file_license
        if not(self.image_copyright):
            self.image_copyright = image_file_copyright

        if (not(image_file_license) and not(self.image_license)) or (not(image_file_copyright) and not(self.image_copyright)):
            print(f"[WARN] The copyright or license of {self.glass_name} is not defined or not found in meta.json")
            self.image_copyright = f"From the {Path(PROJ_DIR.name)}"
            self.image_license = "UNKNOWN LICENSE"


    def get_sprite(self, name = str, color: str = "") -> os.PathLike | None:
        if not(color):
            print(f"[INFO] There is no liquid color for {name}. Skip")
            return None

        r, g, b, a = ImageColor.getcolor(color, "RGBA")

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
def check_and_reencode_utf_sig(file: str | os.PathLike) -> None:
    u = UniversalDetector()
    u.reset()

    with open(file, 'rb') as bfile:
        for line in bfile:
            u.feed(line)
            if u.done: break
    u.close()

    if u.result["encoding"] == "UTF-8-SIG":
        print(f"[WARN] Found UTF-8-SIG in {file} \nChange encoding to UTF-8 (removing BOM)")
        content_sig_file = Path(file).read_text(encoding="UTF-8-SIG")
        new_file = Path(file).with_suffix(".tmp")
        new_file.touch()

        Path(new_file).write_text(content_sig_file, encoding="UTF-8")
        Path(new_file).replace(file)
        print("Encoding changed successfully")

def get_metadata(file: str | os.PathLike, mode: str = "copyright") -> tuple | bool:
    check_and_reencode_utf_sig(file)

    with open(file, "r") as metadata_content:
        data = json.loads(metadata_content.read())

    delays = None
    for key, value in data.items():
        match key:
            case "copyright": copyright_data = value
            case "license": license_data = value
            case "size": M, N = value["x"], value["y"]
        if key == "states" and "delays" in value[0]: delays = value[0]["delays"]

    match mode:
        case "copyright":
            return copyright_data, license_data
        case "anim":
            return M, N, delays
        case "ifanim":
            return True if delays else False

def save_sprite(sprite: Image.Image, name: str, image_copyright: str, image_license: str, glass_name: str = "") -> os.PathLike:
    metadata = PngInfo()
    metadata.add_text("Copyright", f"{glass_name or ''}{name}\n{image_copyright} License: {image_license}")

    sprite = sprite.resize((256, 256), Image.NEAREST)
    sprite.save(SRTE_DIR.joinpath(f"{name}_{glass_name or ''}.png"), pnginfo=metadata)
    return SRTE_DIR.joinpath(f"{name}_{glass_name or ''}.png")

def save_anim(sprite: Image.Image, name: str, M: int, N: int, delays: list, image_copyright: str, image_license: str) -> os.PathLike:
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

    metadata_text = f"{name}\n{image_copyright} License: {image_license}"
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
