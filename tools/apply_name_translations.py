import os
import sys
import traceback

import pandas
from colorama import init, Fore
from pandas import DataFrame, ExcelWriter

init(autoreset=True)

messages = ["""CatSystem2 Simple tools (names translation tool) by ShereKhanRomeo\n
HUGE thanks to Trigger-Segfault for explaining and tool links

This tool will take translated names from `nametable.xlsx` file and apply them to all `.xlsx` files in`translate here\\clean texts` folder.
`Repeat voice` button (speaker icon) won't work if names in `.cst` scripts differ from those in `nametable.csv`.
Even if first time voicing worked correctly.
This tool makes it easier to ensure that compatibility.

If you found out that name translation needs to be changed (found new info during translation),
you still can change name translation in `nametable.xlsx` table and run this tool again.
It will update all names again, keeping all your already translated lines intact.

{0}After applying names translations to `.xslx` text file DO NOT edit names there!
They may contain special characters and widespaces (different from "spacebar" ones) needed for game engine's formatting.
Edit names only in 'nametable.xlsx', then run this tool again.

{1}If you sure you want to apply names translations, press Enter...""",

            "Copying files into 'extracted' folder and unpacking 'int'-archives may take up to 1 minute per file...",
            "Copying {0}...",
            "Processing {0}...",
            "Removing temporary files...",
            "Sorting extracted files...",
            Fore.GREEN + "Done! Program will be closed now.",
            Fore.YELLOW + "Following tools are missing: {0}\nDownload or unpack archive again.",
            Fore.YELLOW + """File 'nametable.csv' was not found after extracting specified archives!
    To find archive with that file you can use 'GARbro' Visual Novels resource browser made by 'morkt' from GitHub.
    Please, find archive with 'nametable.csv' since it is mandatory for ingame features and next translation steps.
    Press Enter to finish the program."""]

# other variables
dir_path = os.path.dirname(os.path.realpath(__file__)).replace("tools", "")
dir_path_tools = dir_path + "tools\\"
dir_path_extracted = dir_path + "source game files\\"
dir_path_extracted_texts = dir_path_extracted + "texts\\"
dir_path_extracted_translations = dir_path_extracted + "translations\\"
dir_path_extracted_manually = dir_path_extracted + "for manual processing\\"
dir_path_extracted_animations = dir_path_extracted_manually + "animations\\"
dir_path_extracted_images = dir_path_extracted_manually + "images\\"
dir_path_extracted_movies = dir_path_extracted_manually + "movies\\"
dir_path_extracted_scripts = dir_path_extracted_manually + "scripts\\"
dir_path_extracted_sounds = dir_path_extracted_manually + "sounds\\"

dir_path_translate_here = dir_path + "translate here\\"
dir_path_translate_here_clean_texts = dir_path_translate_here + "clean texts\\"
dir_path_translate_here_other_files = dir_path_translate_here + "your files AS IS\\"
dir_path_translate_here_other_files_sounds = dir_path_translate_here_other_files + "sounds\\"
dir_path_translate_here_other_files_movies = dir_path_translate_here_other_files + "movies\\"
dir_path_translate_here_other_files_images = dir_path_translate_here_other_files + "images\\"
dir_path_translate_here_other_files_other = dir_path_translate_here_other_files + "other\\"

TRANSLATION_LINE_PATTERN = "translation for line #{0}"
ORIGINAL_LINE_PATTERN = "original line #{0}"
TEXT_LINE_END1 = "\\fn\r\n"
TEXT_LINE_END2 = "\\@\r\n"
SCENE_LINESTART1 = "\tscene "
SCENE_LINESTART2 = "\tstr 3 "  # for Grisaia1 steam version
SCENE_LINESTART3 = "\tstr 155 "  # for Grisaia1 unrated version
WRITE_TRANSLATION_HERE = "(write translation here)"
CHOICE_OPTION = "choice_option"
SCENE_TITLE = "scene_title"
EMPTY_CHARACTER_NAME = "leave_empty"

game_main = "cs2.exe"
hgx2bmp_exe = "hgx2bmp.exe"
zlib1_dll = "zlib1.dll"
exzt_exe = "exzt.exe"
exkifint_v3_exe = "exkifint_v3.exe"
cs2_decompile_exe = "cs2_decompile.exe"

# i am ignoring kx2.ini archive for now, since i have no idea about .kx2-files it has inside
temp_archives = ["scene.int", "config.int", "update00.int", "update01.int", "update02.int", "update03.int",
                 "update04.int", "update05.int", "update06.int", "update07.int", "update08.int", "update09.int",
                 "update10.int", "update11.int", "update12.int", "update13.int", "update14.int", "update15.int"]
temp_files = temp_archives.copy()
temp_files.append(game_main)
temp_tools = [hgx2bmp_exe, zlib1_dll, exzt_exe, exkifint_v3_exe, cs2_decompile_exe]
optional_voice_packages = []

xlsx_original_names = []
xlsx_translated_names = []


def press_any_key():
    skip = input()


def check_all_tools_intact():
    missing_files = ""
    for tool in temp_tools:
        if not os.path.exists(dir_path_tools + tool):
            missing_files += tool + " "
    if len(missing_files) > 0:
        print(str.format(messages[7], missing_files))
        press_any_key()
        sys.exit(0)
    nametable_xlsx = dir_path_translate_here + 'nametable.xlsx'
    if not os.path.exists(nametable_xlsx) or not os.path.isfile(nametable_xlsx):
        print(messages[8])  # nametable not found
        press_any_key()
        sys.exit(0)


def translate_name(_name_to_translate: str, _original_names, _translated_names):
    for i in range(len(_original_names)):
        # need to check and replace whole string, not just parts of it, like when using .replace()
        if _name_to_translate == _original_names[i] and not _translated_names[i] == "(translate name here)":
            return _translated_names[i]
    return _name_to_translate


def apply_names_translations_nametable():
    global xlsx_original_names, xlsx_translated_names
    nametable_csv = dir_path_extracted + 'nametable.csv'
    nametable_xlsx = dir_path_translate_here + 'nametable.xlsx'
    print(str.format(messages[3], 'nametable.xlsx'))
    xlsx_file = pandas.ExcelFile(nametable_xlsx)
    df1 = xlsx_file.parse(xlsx_file.sheet_names[0])
    xlsx_original_names = list(df1[df1.columns[0]]).copy()
    xlsx_translated_names = list(df1[df1.columns[2]]).copy()

    df0 = pandas.read_csv(nametable_csv, encoding='ShiftJIS')
    column0_array = df0.columns[0].split('\t')
    jp_brackets0 = False
    if len(column0_array) > 1:
        if "【" in column0_array[1] or "】" in column0_array[1]:
            jp_brackets0 = True
            name0 = column0_array[1].strip("【】").replace("\\fs　\\fn", " ")
        else:
            name0 = column0_array[1].replace("\\fs　\\fn", " ")
        translated_name0 = translate_name(name0, xlsx_original_names, xlsx_translated_names).replace(" ", "\\fs　\\fn").replace('ë', 'ё')
        if jp_brackets0:
            translated_name0 = "【" + translated_name0 + "】"
        column0_array[1] = translated_name0
    df0.rename(columns={df0.columns[0]: "\t".join(column0_array)}, inplace=True)

    for line_array in df0.to_numpy():
        array = line_array[0].split('\t')
        jp_brackets = False
        if len(array) > 1:
            if "【" in array[1] or "】" in array[1]:
                jp_brackets = True
                name = array[1].strip("【】").replace("\\fs　\\fn", " ")
            else:
                name = array[1].replace("\\fs　\\fn", " ")
            translated_name = translate_name(name, xlsx_original_names, xlsx_translated_names).replace(" ", "\\fs　\\fn").replace('ë', 'ё')
            if jp_brackets:
                translated_name = "【" + translated_name + "】"
            array[1] = translated_name
            line_array[0] = "\t".join(array)

    df0.to_csv(dir_path_translate_here + 'nametable.csv', encoding='ShiftJIS', index=False)


def apply_names_translations_texts():
    global xlsx_original_names, xlsx_translated_names

    for filename in os.listdir(dir_path_translate_here_clean_texts):
        file_xlsx = dir_path_translate_here_clean_texts + filename
        if os.path.isfile(file_xlsx) and file_xlsx.endswith(".xlsx"):
            print(str.format(messages[3], filename))
            xlsx_file = pandas.ExcelFile(file_xlsx)
            df0 = xlsx_file.parse(xlsx_file.sheet_names[0])
            column1_ids = list(df0[df0.columns[0]]).copy()
            column2_names = []
            column2_names_old = list(df0[df0.columns[1]]).copy()
            column3_lines = list(df0[df0.columns[2]]).copy()

            while len(column2_names_old) > 1:
                column2_names.append(column2_names_old.pop(0))
                column2_names.append(translate_name(column2_names_old.pop(0).replace("\\fs　\\fn", " "), xlsx_original_names, xlsx_translated_names).replace(" ", "\\fs　\\fn"))

            df = DataFrame({"Lines numbers": column1_ids, "Character name": column2_names, "Line text": column3_lines})
            writer = ExcelWriter(file_xlsx)
            df.to_excel(writer, sheet_name='sheetName', index=False, na_rep='NaN')
            for column in df:
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['sheetName'].set_column(col_idx, col_idx, column_length)
            writer.close()


# core logic
try:
    check_all_tools_intact()
    print(str.format(messages[0], Fore.YELLOW, Fore.RESET))
    press_any_key()
    apply_names_translations_nametable()
    apply_names_translations_texts()

except Exception as error:
    print("ERROR - " + str("".join(traceback.format_exception(type(error),
                                                              value=error,
                                                              tb=error.__traceback__))).split(
        "The above exception was the direct cause of the following")[0])
finally:
    print(messages[6])  # done
