import yaml

from any_yaml import Loader

from project_dirs import *
from rw_func import *

if __name__ == "__main__":
    print("[ERR] Run the RUN.py")
    exit()
else:
    print("[INFO] Loading data:")


# takes "dict_generator" as string with itareble "data"
def get_data(path, dict_generator):
    print(f"[INFO] - {path.name}")
    dct = {}
    files = sorted(path.glob("**/*.yml"))

    for file in files:
        check_and_reencode_utf_sig(file)

        with open(file) as file:
            data = yaml.load(file, Loader=Loader)

        for i in range(len(data)):
            dct.update(eval(dict_generator))

    return dct


reag_dict_gen = '{reagent["id"]: {key: value for key, value in reagent.items() if key != "id"} for reagent in data}'
reagents = get_data(REAG_DIR, reag_dict_gen)
reag_groups = {reagent["group"] for reagent in reagents.values() if "group" in reagent}
reag_groups.add("reagent")

recp_dict_gen = '{recipes["id"]: {key: value["amount"] for key, value in recipes["reactants"].items()} for recipes in data if "reactants" in recipes}'
recipes = get_data(RECP_DIR, recp_dict_gen)


print("[INFO] Finished")
