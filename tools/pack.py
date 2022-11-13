import codecs
import os
import shutil
import subprocess
import sys
import traceback
from subprocess import call

import pandas
from colorama import init, Fore

init(autoreset=True)

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("tools", "")
dir_path_package = dir_path + "package\\"
dir_path_tools = dir_path + "tools\\"
dir_path_extracted = dir_path + "source game files\\"
dir_path_extracted_texts = dir_path_extracted + "texts\\"
dir_path_extracted_manually = dir_path_extracted + "for manual processing\\"
dir_path_extracted_animations = dir_path_extracted_manually + "animations\\"
dir_path_extracted_images = dir_path_extracted_manually + "images\\"
dir_path_extracted_movies = dir_path_extracted_manually + "movies\\"
dir_path_extracted_scripts = dir_path_extracted_manually + "scripts\\"
dir_path_extracted_sounds = dir_path_extracted_manually + "sounds\\"

dir_path_translations = dir_path + "translate here\\"
dir_path_translations_clean_texts = dir_path_translations + "clean texts\\"
dir_path_translations_other_files = dir_path_translations + "your files AS IS\\"
dir_path_translations_other_files_sounds = dir_path_translations_other_files + "sounds\\"
dir_path_translations_other_files_movies = dir_path_translations_other_files + "movies\\"
dir_path_translations_other_files_images = dir_path_translations_other_files + "images\\"
dir_path_translations_other_files_other = dir_path_translations_other_files + "other\\"

empty_character_name = "leave_empty"
WRITE_TRANSLATION_HERE = "(write translation here)"

mc_exe = "mc.exe"
makeint_exe = "MakeInt.exe"
temp_tools = [mc_exe, makeint_exe]

messages = ["""CatSystem2 Simple tools (packing tool) by ShereKhanRomeo\n
HUGE thanks to Trigger-Segfault for explaining and tool links
check his wiki here https://github.com/trigger-segfault/TriggersTools.CatSystem2/wiki \n
All files from "extracted" folder will be compiled into archive with number of your choice.

Note that if you enter single-digit number 'X' for archive, it will be converted to double-digit number with leading zero: '0X'.
It is OK and made just for CatSystem2 game engine compatibility.

Press Enter to start...""",
            Fore.GREEN + "Done! Program will be closed now.",
            Fore.LIGHTRED_EX + "Following tools are missing: {0}\nDownload or unpack archive again.",
            "Processing {0}...",
            "Packing texts...",
            "Packing images...",
            "Packing movies...",
            "Packing scripts...",
            "\nEnter number for resulting archive name (choose from '4' to '99'; leave empty for '13' by default): ",
            Fore.YELLOW + "Your input was incorrect in some way. Using number '13' by default."]


# functions
def press_any_key():
    skip = input()


def create_if_not_exists(_path_to_file_or_dir: str):
    if not os.path.exists(_path_to_file_or_dir):
        os.mkdir(_path_to_file_or_dir)


def check_all_tools_intact():
    missing_files = ""
    for tool in temp_tools:
        if not os.path.exists(dir_path_tools + tool):
            missing_files += tool + " "
    if len(missing_files) > 0:
        print(str.format(messages[2], missing_files))
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


def prepare_to_pack_texts():
    os.chdir(dir_path)
    for filename in os.listdir(dir_path_translations_clean_texts):
        # first - get translations from .xlsx files
        if os.path.isfile(dir_path_translations_clean_texts + filename) and filename.endswith(".xlsx") and not filename.startswith("~"):
            print(str.format(messages[3], filename))
            df = pandas.ExcelFile(dir_path_translations_clean_texts + filename) \
                .parse(pandas.ExcelFile(dir_path_translations_clean_texts + filename).sheet_names[0])
            text_lines = list(df[df.columns[2]]).copy()
            text_names = list(df[df.columns[1]]).copy()
            text_file = filename.replace(".xlsx", ".txt")

            encodingShiftJIS = "ShiftJIS"
            file_lines = []
            # second - get original texts from .txt files in `extracted\texts\`
            if os.path.exists(dir_path_extracted_texts + text_file):
                with codecs.open(dir_path_extracted_texts + text_file, mode="r", encoding=encodingShiftJIS) as source_txt_file:
                    file_lines = source_txt_file.readlines()
                    source_txt_file.close()
                # third - write resulting .txt files with translation into `package` folder
                with codecs.open(dir_path_package + text_file, mode="w", encoding=encodingShiftJIS) as result_txt_file:
                    for file_line in file_lines:
                        if len(text_lines) > 0 and text_lines[0] in file_line and text_lines[1] != WRITE_TRANSLATION_HERE:
                            text_to_replace = text_lines.pop(0)
                            replacement_text = text_lines.pop(0) \
                                .replace('№', '#') \
                                .replace('…', '...') \
                                .replace('"', '“') \
                                .replace('ë', 'ё') \
                                .replace("'", '`')

                            name_to_replace = text_names.pop(0)
                            replacement_name = text_names.pop(0)

                            # if not scene title - wrap each word after first one with []
                            if name_to_replace != "scene_title":
                                replacement_list = replacement_text.split(' ')
                                if len(replacement_list) > 1:
                                    replacement_text = replacement_list.pop(0) + " ["
                                    replacement_text += "] [".join(replacement_list) + ']'
                                else:
                                    replacement_text = replacement_text

                            file_line = file_line.replace(text_to_replace, replacement_text)
                            file_line = file_line.replace(name_to_replace, replacement_name)
                            # print("(DEBUG)writing line: " + file_line)
                        result_txt_file.write(file_line)
                        result_txt_file.flush()
            else:
                raise Exception(str.format("ERROR - Missing required file = {0}.\nPlease, restore the file into {1} folder or do unpacking process again!", text_file, dir_path_extracted_texts))
    # then use mc.exe
    os.chdir(dir_path_package)
    print(messages[4])
    shutil.copy(dir_path_tools + mc_exe, dir_path_package + mc_exe)
    call([mc_exe, "*"], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_package, ".txt")
    delete_file(dir_path_package + mc_exe)
    os.chdir(dir_path)


def copy_all_files_from_to(_from, _to):
    if os.path.exists(_from) and os.path.isdir(_from) and os.path.exists(_to) and os.path.isdir(_to):
        for filename in os.listdir(_from):
            if os.path.isfile(_from + filename):
                print("Preparing " + filename)
                shutil.copy(_from + filename, _to + filename)


def pack_int_archive():
    os.chdir(dir_path)
    shutil.copy(dir_path_tools + makeint_exe, dir_path + makeint_exe)
    #copy_all_files_from_to(dir_path_translations_other_files_images, dir_path_package)
    #copy_all_files_from_to(dir_path_translations_other_files_movies, dir_path_package)
    #copy_all_files_from_to(dir_path_translations_other_files_sounds, dir_path_package)
    #copy_all_files_from_to(dir_path_translations_other_files_other, dir_path_package)
    # todo add archive number
    archive_number = input(messages[8]) or "13"
    if not archive_number.isdigit():
        print(messages[9])
        archive_number = "13"
    if len(archive_number) == 1:
        archive_number = "0" + archive_number
    archive_name = str.format("update{0}.int", archive_number)
    print(str.format("Packing archive {0}...", archive_name))
    subprocess.call(str.format("makeint {0} \"{1}\" \"{2}\" \"{3}\" \"{4}\" \"{5}\" \"{6}\"",
                               archive_name,
                               dir_path_translations_other_files_movies + '*',
                               dir_path_translations_other_files_images + '*',
                               dir_path_translations_other_files_sounds + '*',
                               dir_path_translations_other_files_other + '*',
                               dir_path_package + '*',
                               dir_path_translations + 'nametable.csv'))
    delete_file(dir_path + makeint_exe)
    clean_files_from_dir(dir_path_package, ".cst")
    clean_files_from_dir(dir_path_package, ".hg3")
    clean_files_from_dir(dir_path_package, ".mpg")
    clean_files_from_dir(dir_path_package, ".ogg")
    clean_files_from_dir(dir_path_package, ".fes")
    clean_files_from_dir(dir_path_package, ".csv")
    clean_files_from_dir(dir_path_package, ".xml")
    clean_files_from_dir(dir_path_package, ".dat")
    clean_files_from_dir(dir_path_package, ".png")
    remove_empty_folders()


# core logic
try:
    check_all_tools_intact()
    # todo add archive number
    print(messages[0])
    press_any_key()
    prepare_to_pack_texts()
    pack_int_archive()

except Exception as error:
    print("ERROR - " + str("".join(traceback.format_exception(type(error),
                                                              value=error,
                                                              tb=error.__traceback__))).split(
        "The above exception was the direct cause of the following")[0])
finally:
    print(messages[1])  # done
