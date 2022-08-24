import codecs
import ctypes
import locale
import os
import shutil
import sys
import traceback
from subprocess import call

import pandas

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("tools", "")
dir_path_extracted = dir_path + "extracted\\"
dir_path_package = dir_path + "package\\"
dir_path_tools = dir_path + "tools\\"
dir_path_extracted_animations = dir_path + "extracted\\animations\\"
dir_path_extracted_images = dir_path + "extracted\\images\\"
dir_path_extracted_movies = dir_path + "extracted\\movies\\"
dir_path_extracted_scripts = dir_path + "extracted\\scripts\\"
dir_path_extracted_sounds = dir_path + "extracted\\sounds\\"
dir_path_extracted_texts = dir_path + "extracted\\texts\\"
dir_path_extracted_clean_texts_for_translations = dir_path + "extracted\\clean texts for translations\\"

empty_character_name = "leave_empty"
WRITE_TRANSLATION_HERE = "(write translation here)"

mc_exe = "mc.exe"
makeint_exe = "MakeInt.exe"
temp_tools = [mc_exe, makeint_exe]

# locales to help more enthusiasts understand this tool
# just create new list with your translation and insert it into "select_locale()"
# locale[0] = intro
# locale[1] = done! Enter to exit
# locale[2] = error missing files, Enter to exit
# locale[3] = processing file
locale_to_use = []
# TODO finish descriptions
locale_ru = ["""Упаковщик ресурсов движка CatSystem2 авторства ShereKhanRomeo\n
ОГРОМНОЕ спасибо Trigger-Segfault за объяснения и ссылки на инструменты
Подробности на его вики: https://github.com/trigger-segfault/TriggersTools.CatSystem2/wiki \n\n
В архив {0} будут упакованы все файлы из папки "extracted" - нажмите Enter, чтобы начать...\n""",
             "Готово! Программа будет закрыта.",
             "Отсутствуют файлы в папке tools: {0}\nСкачайте или извлеките архив заново.",
             "Обработка {0}...",
             "Упаковка текстов...",
             "Упаковка изображений...",
             "Упаковка видеофайлов...",
             "Упаковка скриптов...",
             "Упаковка итогового архива {0}..."]

locale_default = ["""Resources unpacker for CatSystem2 games by ShereKhanRomeo\n
HUGE thanks to Trigger-Segfault for explaining and tool links
check his wiki here https://github.com/trigger-segfault/TriggersTools.CatSystem2/wiki \n\n
All files from "extracted" folder will be compiled into {0} archive -  press Enter to start...""",
                  "Done! Program will be closed now.",
                  "Following tools are missing: {0}\nDownload or unpack archive again.",
                  "Processing {0}...",
                  "Packing texts...",
                  "Packing images...",
                  "Packing movies...",
                  "Packing scripts...",
                  "Packing resulting archive {0}..."]


# functions
def press_any_key():
    skip = input()


def create_if_not_exists(_path_to_file_or_dir: str):
    if not os.path.exists(_path_to_file_or_dir):
        os.mkdir(_path_to_file_or_dir)


def select_locale():
    global locale_to_use
    match locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]:
        case 'ru_RU':
            locale_to_use = locale_ru
            return
        case _:
            locale_to_use = locale_default
            return


def check_all_tools_intact():
    missing_files = ""
    for tool in temp_tools:
        if not os.path.exists(dir_path_tools + tool):
            missing_files += tool + " "
    if len(missing_files) > 0:
        print(str.format(locale_to_use[2], missing_files))
        press_any_key()
        sys.exit(0)
    create_if_not_exists(dir_path_package)


def delete_file(path_to_file: str):
    if os.path.exists(path_to_file):
        os.chmod(path_to_file, 0o777)
        os.remove(path_to_file)


def remove_empty_folders():
    # also remove empty folders
    for pth in os.listdir(dir_path):
        if os.path.isdir(dir_path + pth):
            with os.scandir(dir_path + pth) as it:
                if not any(it):
                    os.rmdir(dir_path + pth)


def clean_files_from_dir(_dir: str, _filetype: str):
    for filename in os.listdir(_dir):
        file = _dir + filename
        if file.endswith(_filetype):
            delete_file(file)


def pack_texts():
    for filename in os.listdir(dir_path_extracted_clean_texts_for_translations):
        # first - get texts from .xlsx files
        if filename.endswith(".xlsx"):
            print(str.format(locale_to_use[3], filename))
            df = pandas.ExcelFile(dir_path_extracted_clean_texts_for_translations + filename) \
                .parse(pandas.ExcelFile(dir_path_extracted_clean_texts_for_translations + filename).sheet_names[0])
            text_lines = list(df[df.columns[2]]).copy()
            text_names = list(df[df.columns[1]]).copy()
            text_file = filename.replace(".xlsx", ".txt")

            encodingShiftJIS = "ShiftJIS"
            file_lines = []
            # second - insert them into their places in .txt files
            if os.path.exists(dir_path_extracted_texts + text_file):
                with codecs.open(dir_path_extracted_texts + text_file, mode="r", encoding=encodingShiftJIS) as file:
                    file_lines = file.readlines()
                    file.close()
                with codecs.open(dir_path_package + text_file, mode="w", encoding=encodingShiftJIS) as file:
                    for file_line in file_lines:
                        # print("DEBUG")
                        # print("looking for: " + text_lines[0])
                        # print("inside line: " + file_line)
                        # press_any_key()
                        if len(text_lines) > 0 and text_lines[0] in file_line and text_lines[1] != WRITE_TRANSLATION_HERE:
                            file_line = file_line.replace(text_lines.pop(0), text_lines.pop(0))
                            file_line = file_line.replace(text_names.pop(0), text_names.pop(0))
                        file.write(file_line)
            else:
                raise Exception(str.format("ERROR - Missing required file = {0}.\nPlease, restore the file into {1} folder or do unpacking process again!", text_file, dir_path_extracted_texts))
    # then use mc.exe
    os.chdir(dir_path_package)
    shutil.copy(dir_path_tools + mc_exe, dir_path_package + mc_exe)
    print(locale_to_use[4])
    call([mc_exe, "*"], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_package, ".txt")
    delete_file(dir_path_package + mc_exe)
    os.chdir(dir_path)


def pack_int_archive():
    shutil.copy(dir_path_tools + makeint_exe, dir_path + makeint_exe)
    print(str.format(locale_to_use[8], "update13.int"))
    call([makeint_exe, "update13.int", dir_path_package + "*"], stdin=None, stdout=None, stderr=None, shell=False)
    delete_file(dir_path + makeint_exe)
    clean_files_from_dir(dir_path_package, ".cst")
    clean_files_from_dir(dir_path_package, ".fes")
    clean_files_from_dir(dir_path_package, ".ogg")
    clean_files_from_dir(dir_path_package, ".hg3")
    remove_empty_folders()


# core logic
try:
    select_locale()
    check_all_tools_intact()
    print(locale_to_use[0])
    press_any_key()
    # pack_images()

    pack_texts()

    pack_int_archive()

except Exception as error:
    print("ERROR - " + str("".join(traceback.format_exception(type(error),
                                                              value=error,
                                                              tb=error.__traceback__))).split(
        "The above exception was the direct cause of the following")[0])
finally:
    # remove_temp_files()
    # remove_empty_folders()
    print(locale_to_use[1])  # done
