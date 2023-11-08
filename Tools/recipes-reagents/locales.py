import re

from project_dirs import *
from pathlib import Path

if __name__ == "__main__":
    print("[ERR] Run the RUN.py")
    exit()


def locale_list(files):
    value_list = []

    for file in files:
        with open(file, mode="rt", encoding="utf-8") as data:
            lines = data.read().splitlines()
            values = [re.split(r"\s*=\s*", line) for line in lines]
            value_list.extend(values)

    i = 0
    while i < len(value_list):
        if len(value_list[i]) <= 1:
            value_list.pop(i)
        else:
            i += 1

    return value_list


print("[INFO] Loading locales:")
locales_en_list = sorted(LOCL_DIR.joinpath("en-US").glob("**/*.ftl"))
locales_ru_list = sorted(LOCL_DIR.joinpath("ru-RU").glob("**/*.ftl"))

print("[INFO] - en...")
locale_en = {
    pair[0]: pair[1] for pair in locale_list(locales_en_list)
}

print("[INFO] - ru...")
locale_ru = {
    pair[0]: pair[1] for pair in locale_list(locales_ru_list)
}

print("[INFO] Finished")

