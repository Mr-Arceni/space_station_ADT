from pathlib import Path

if __name__ == "__main__":
    print("[ERR] Run the RUN.py")
    exit()


if not(Path(__file__).parents[2].joinpath("Resources/Prototypes/Recipes").exists()) or not(Path(__file__).parents[2].joinpath("Resources/Prototypes/Reagents").exists()):
    print("'[ERR] ../../Resources/Prototypes/Recipes' or '../../Resources/Prototypes/Reagents' were not found. \n\nSpecify the absolute path to the project, or move this file to [PROJECT_DIR]/Tools/recipes-reagents \nEnter [0] to exit")
    entered_path = input()

    while not(Path(entered_path).is_dir()) or not(Path(entered_path).joinpath("Resources/Prototypes/Recipes").exists()) or not(Path(entered_path).joinpath("Resources/Prototypes/Reagents").exists()):
        if entered_path == "0": exit()
        print("Entered path is not a dir, or does not exist, or not specified to SS14 project dir \nTry again")
        entered_path = input()
    PROJ_DIR = Path(entered_path)

else:
    PROJ_DIR = Path(__file__).parents[2]

RECP_DIR = PROJ_DIR.joinpath("Resources/Prototypes/Recipes")
REAG_DIR = PROJ_DIR.joinpath("Resources/Prototypes/Reagents")
LOCL_DIR = PROJ_DIR.joinpath("Resources/Locale/")

SAVE_DIR = PROJ_DIR.joinpath("Tools/recipes-reagents")
SRTE_DIR = SAVE_DIR.joinpath("sprites")

if not(SRTE_DIR.joinpath("animations").exists()):
    SRTE_DIR.joinpath("animations").mkdir(parents=True)
