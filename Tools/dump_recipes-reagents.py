import yaml
import xlsxwriter

from any_yaml import Loader
from pathlib import Path
from chardet import UniversalDetector

RECP_DIR = Path(__file__).parents[1].joinpath("Resources/Prototypes/Recipes")
REGN_DIR = Path(__file__).parents[1].joinpath("Resources/Prototypes/Reagents")

if not(RECP_DIR.exists()) or not(REGN_DIR.exists()):
    print("'../Resources/Prototypes/Recipes' or '../Resources/Prototypes/Reagents' were not found. \nTerminate program")
    exit()


# Files with BOM cause a yaml.scanner.scannererror exception
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


reac_files = sorted(RECP_DIR.joinpath("Reactions").glob("*.yml"))

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
