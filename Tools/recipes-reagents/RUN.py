import xlsxwriter

from pathlib import Path

from project_dirs import *
from locales import *
from rw_func import *
from glasses import *
from data import *
from xls_func import *
from xls_format import *

path_file = "Reagents.xlsx"

with xlsxwriter.Workbook(SAVE_DIR.joinpath(path_file)) as xls_file:
    xls_worksheets = {reag_group: xls_file.add_worksheet(reag_group) for reag_group in reag_groups}
    order = {reag_group: 1 for reag_group in reag_groups} # Order counter for each group
    headers = {
        "ID": {"width": 12},
        "Цвет": {"width": 8},
        "Название en/ru": {"width": 15},
        "Описание en/ru": {"width": 30},
        "Физ. описание en/ru": {"width": 20},
        "Метаморф-спрайт": {"width": 8},
        "Анимированный спрайт": {"width": 8},
        "Рецепт": {
            "width": 16,
            "format": {
                "align": "left",
                "valign": "top",
                "text_wrap": "True"
            }
        },
        "Определяемый?": {"width": 5},
        "Скользкий?": {"width": 5},
        "Абстрактный?": {"width": 5},
        "Свойства": {
            "width": 20,
            "format": {
                "align": "left",
                "valign": "top",
                "text_wrap": "True"
            }
        },
    }

    main_row_format = get_xls_format(main_row_reagent_format, xls_file)
    true_format = get_xls_format(true_format, xls_file)
    false_format = get_xls_format(false_format, xls_file)
    first_row_format = get_xls_format(blue_reagent_format, xls_file, "multi")
    second_row_format = get_xls_format(red_reagent_format, xls_file, "multi")

    for worksheet in xls_worksheets.values():
        worksheet.write_row(0, 0, headers.keys(), main_row_format)
        k = 0
        for col in headers.values():
            if "format" in col:
                worksheet.set_column(k, k, col["width"], xls_file.add_format(col["format"]))
            else:
                worksheet.set_column(k, k, col["width"])
            k += 1

    for reagent, properties in reagents.items():
        xls_write_reagent(reagent, properties, order, xls_worksheets, first_row_format, second_row_format, true_format, false_format)

    print("[INFO] Saving...")
print(f"[INFO] Complete xlsx: {Path(path_file)}")
