import re

from project_dirs import *
from pathlib import Path

if __name__ == "__main__":
    print("[ERR] Run the RUN.py")
    exit()
else:
    print("[INFO] Loading locales:")


# return dict loaded from Resources/Locale/name
def create_locale(name):
    print(f"[INFO] - {name}...")
    files = sorted(LOCL_DIR.joinpath(name).glob("**/*.ftl"))

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

    return {pair[0]: pair[1] for pair in value_list}

def get_locale(lang, key):
    for locale in list_locales.keys():
        if locale == lang:
            if key in list_locales[lang]:
                return list_locales[lang][key]
            else:
                print(f"[WARN] There is no {key} in {lang} locales")
                return ""
    raise ValueError(f"{lang} in locales is not defined \nExisting options: {list_locales.keys()}")


locale_en = create_locale("en-US")
locale_ru = create_locale("ru-RU")

list_locales = {
    "en": locale_en,
    "ru": locale_ru
}

print("[INFO] Finished")
