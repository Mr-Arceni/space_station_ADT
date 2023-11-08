from rw_func import SpriteOfLiquidContainer
from project_dirs import *

if __name__ == "__main__":
    print("[ERR] Run the RUN.py")
    exit()


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
