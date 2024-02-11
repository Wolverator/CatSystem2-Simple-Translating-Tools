import codecs
import os
import shutil
import sys
import traceback
from sys import executable
from os import path
from re import compile, escape, IGNORECASE
from subprocess import call, DEVNULL

import pandas
from colorama import init, Fore

init(autoreset=True)

# other variables
dir_path = path.dirname(path.realpath(__file__)).replace("tools", "")
print("Path: " + dir_path)
dir_path_tools = dir_path + "tools\\"
dir_path_package = dir_path + "package\\"
dir_path_extracted = dir_path + "source game files\\"
dir_path_extracted_texts = dir_path_extracted + "texts\\"
dir_path_extracted_localization_texts = dir_path_extracted + "localization texts\\"
dir_path_extracted_manually = dir_path_extracted + "for manual processing\\"
dir_path_extracted_animations = dir_path_extracted_manually + "animations\\"
dir_path_extracted_images = dir_path_extracted_manually + "images\\"
dir_path_extracted_movies = dir_path_extracted_manually + "movies\\"
dir_path_extracted_scripts = dir_path_extracted_manually + "scripts\\"
dir_path_extracted_sounds = dir_path_extracted_manually + "sounds\\"

dir_path_translate_here = dir_path + "translate here\\"
dir_path_translate_here_clean_texts = dir_path_translate_here + "clean texts\\"
dir_path_translate_here_clean_localization_texts = dir_path_translate_here + "clean localization texts\\"
dir_path_translate_here_other_files = dir_path_translate_here + "your files AS IS\\"
dir_path_translate_here_other_files_sounds = dir_path_translate_here_other_files + "sounds\\"
dir_path_translate_here_other_files_movies = dir_path_translate_here_other_files + "movies\\"
dir_path_translate_here_other_files_images = dir_path_translate_here_other_files + "images\\"
dir_path_translate_here_other_files_other = dir_path_translate_here_other_files + "other\\"

empty_character_name = "leave_empty"
WRITE_TRANSLATION_HERE = "(write translation here)"

game_main = None
mc_exe = "mc.exe"
cstl_tool_zip = "cstl_tool.zip"
temp_tools = [mc_exe, cstl_tool_zip]

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
            "\nEnter number for resulting archive name (choose from '4' to '99'; leave empty for '04' by default): ",
            Fore.YELLOW + "Your input was incorrect in some way. Using number '13' by default."]


# functions
def press_any_key():
    skip = input()


def create_if_not_exists(_path_to_file_or_dir: str):
    if not os.path.exists(_path_to_file_or_dir):
        os.mkdir(_path_to_file_or_dir)


def check_all_tools_intact():
    global game_main
    missing_files = ""
    for tool in temp_tools:
        if not os.path.exists(dir_path_tools + tool):
            missing_files += tool + " "
    if len(missing_files) > 0:
        print(str.format(messages[2], missing_files))
        press_any_key()
        sys.exit(0)
    create_if_not_exists(dir_path_package)

    if path.exists(dir_path + "\\cs2.exe"):
        game_main = "cs2.exe"
    if path.exists(dir_path + "\\amakanoPlus.exe"):
        game_main = "amakanoPlus.exe"
    if path.exists(dir_path + "\\grisaia.exe"):
        game_main = "grisaia.exe"
    if path.exists(dir_path + "\\Grisaia2.exe"):
        game_main = "Grisaia2.exe"
    if path.exists(dir_path + "\\Grisaia3.exe"):
        game_main = "Grisaia3.exe"
    if path.exists(dir_path + "\\YukikoiMelt.exe"):
        game_main = "YukikoiMelt.exe"
    if path.exists(dir_path + "\\rinko.exe"):
        game_main = "rinko.exe"
    if path.exists(dir_path + "\\ISLAND.exe"):
        game_main = "ISLAND.exe"

    if game_main == "None":
        print(Fore.RED + "Main game executable is not found!\n" +
              Fore.YELLOW + "If it's '[game name].exe' - please rename it into 'cs2.exe'\n"
              "Unpacker will be closed now...")
        exit(0)
    else:
        print(Fore.GREEN + "Found main game executable: " + game_main)


def delete_file(path_to_file: str):
    if os.path.exists(path_to_file):
        os.chmod(path_to_file, 0o777)
        os.remove(path_to_file)


def remove_empty_folders():
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


def pack_from_ini_to_cstl_files():
    print("Processing .ini files...")
    os.chdir(dir_path)
    ini_files = os.listdir(dir_path_translate_here_clean_localization_texts)
    for filename in ini_files:
        # write translations from .ini files to .cstl files into `package` folder
        if len(ini_files) > 0 and os.path.isfile(dir_path_translate_here_clean_localization_texts + filename)\
                and filename.endswith(".ini")\
                and not filename.startswith("~"):
            print(str.format(messages[3], filename))
            call([
                executable,
                dir_path_tools + cstl_tool_zip,
                "-c", dir_path_translate_here_clean_localization_texts + filename,
                "-o", dir_path_package + filename.replace(".ini", ".cstl")
            ], stdin=None, stdout=DEVNULL, stderr=None, shell=False)


def pack_from_xlsx_to_cst_files():
    #print("Processing .xlsx files...")
    os.chdir(dir_path)
    for filename in os.listdir(dir_path_translate_here_clean_texts):
        # first - get translations from .xlsx files
        if os.path.isfile(dir_path_translate_here_clean_texts + filename) and filename.endswith(".xlsx") and not filename.startswith("~"):
            print(str.format(messages[3], filename))
            df = pandas.ExcelFile(dir_path_translate_here_clean_texts + filename) \
                .parse(pandas.ExcelFile(dir_path_translate_here_clean_texts + filename).sheet_names[0])
            text_lines = list(df[df.columns[2]]).copy()
            text_names = list(df[df.columns[1]]).copy()
            text_file = filename.replace(".xlsx", ".txt")

            encoding_write = "ShiftJIS"
            encoding_read = "ShiftJIS"
            if game_main == "ISLAND.exe":
                encoding_read = "ANSI"
            # second - get original texts from .txt files in `extracted\texts\`
            if os.path.exists(dir_path_extracted_texts + text_file):
                #print(Fore.CYAN + str(text_lines))
                with codecs.open(dir_path_extracted_texts + text_file, mode="r", encoding=encoding_read) as source_txt_file:
                    file_lines = source_txt_file.readlines()
                    source_txt_file.close()
                # third - write resulting .txt files with translation into `package` folder
                with codecs.open(dir_path_package + text_file, mode="w", encoding=encoding_write) as result_txt_file:
                    for file_line in file_lines:
                        if (len(text_lines) > 0) and (text_lines[0] in file_line):
                            text_to_replace = text_lines.pop(0)
                            replacement_text = text_lines.pop(0)

                            name_to_replace = text_names.pop(0)
                            replacement_name = text_names.pop(0)

                            if (replacement_text == WRITE_TRANSLATION_HERE):
                                continue
                            else:
                                print(Fore.GREEN + file_line)
                                replacement_text = replacement_text.replace('№', '#') \
                                                                    .replace('…', '...') \
                                                                    .replace('"', '“') \
                                                                    .replace('ë', 'ё') \
                                                                    .replace("'", '`') \
                                                                    .replace('—', '―') \
                                                                    .replace('«', '"') \
                                                                    .replace('»', '"')
                                # if not scene title - wrap each word after first one with []
                                if name_to_replace == "scene_title":
                                    replacement_text = replacement_text.replace(' ', '_')

                                else:
                                    replacement_list = replacement_text.split(' ')
                                    if len(replacement_list) > 1:
                                        replacement_text = replacement_list.pop(0) + " ["
                                        replacement_text += "] [".join(replacement_list) + ']'
                                    else:
                                        replacement_text = replacement_text
                                file_line = file_line.replace(text_to_replace, replacement_text)
                                file_line = file_line.replace(name_to_replace, replacement_name)
                                print(Fore.GREEN + file_line)
                        try:
                            result_txt_file.write(file_line)
                            result_txt_file.flush()
                        except UnicodeEncodeError as uniError:
                            print(Fore.RED + "A problem occurred while processing line:|" + Fore.RESET + file_line + Fore.RED + "|")
                            print(Fore.YELLOW + "Seems like there is a symbol that cannot be encoded into game files encoding.\n"
                                                "Please, let me know about this error at Git Issues and specify the unicode code of character that caused the problem!")
                            raise uniError
            else:
                raise Exception(str.format("ERROR - Missing required file = {0}.\nPlease, restore the file into {1} folder or do unpacking process again!", text_file, dir_path_extracted_texts))
    # then use mc.exe
    os.chdir(dir_path_package)
    print(messages[4])
    input()
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
    archive_number = input(messages[8]) or "4"
    if not archive_number.isdigit():
        print(messages[9])
        archive_number = "4"
    if len(archive_number) == 1:
        archive_number = "0" + archive_number
    archive_name = str.format("update{0}.int", archive_number)
    print(str.format("Packing archive {0}...", archive_name))
    files = [dir_path_package + '*',  # main text files (.cst and .cstl)
             dir_path_translate_here_other_files_sounds + '*',
             dir_path_translate_here_other_files_images + '*',
             dir_path_translate_here_other_files_movies + '*',
             dir_path_translate_here_other_files_other + '*']
    if os.path.exists(dir_path_translate_here + 'nametable.csv'):
        files.append(dir_path_translate_here + 'nametable.csv')
    makeint(archive_name, files)
    clean_files_from_dir(dir_path_package, ".cst")
    clean_files_from_dir(dir_path_package, ".cstl")
    clean_files_from_dir(dir_path_package, ".ini")
    clean_files_from_dir(dir_path_package, ".hg3")
    clean_files_from_dir(dir_path_package, ".mpg")
    clean_files_from_dir(dir_path_package, ".ogg")
    clean_files_from_dir(dir_path_package, ".fes")
    clean_files_from_dir(dir_path_package, ".csv")
    clean_files_from_dir(dir_path_package, ".xml")
    clean_files_from_dir(dir_path_package, ".dat")
    clean_files_from_dir(dir_path_package, ".png")
    remove_empty_folders()


def findfiles(wildcards: list) -> list:
    files = []
    for path in wildcards:
        if '*' not in path and '?' not in path:
            # Just a regular file path
            files.append(path)
        else:
            filedir, name = os.path.split(path)
            regex = compile(escape(name).replace(r'\*', '.*').replace(r'\?', '.?'), IGNORECASE)
            for file in os.listdir(filedir or '.'):
                if regex.search(file):
                    # Don't join path if filedir is empty
                    files.append(os.path.join(filedir, file) if filedir else file)
    return files


def makeint(archive: str, wildcards: list):
    files = findfiles(wildcards)
    return writeint(archive, files)


def writeint(archive: str, files: list):
    import os.path
    from struct import Struct
    KIFHDR = Struct('<4sI')
    KIFENTRY = Struct('<64sII')

    class Entry:
        def __init__(self, file: str):
            self.path = file
            self.name = os.path.basename(file)
            self.offset = 0
            self.length = os.path.getsize(file)

        def pack(self):
            return KIFENTRY.pack(self.name.encode('cp932'), self.offset, self.length)

    entries = [Entry(file) for file in files]
    offset = KIFHDR.size + KIFENTRY.size * len(files)
    for entry in entries:
        entry.offset = offset
        offset += entry.length
    with open(archive, 'wb+') as fw:
        fw.write(KIFHDR.pack(b'KIF\x00', len(files)))
        for entry in entries:
            fw.write(entry.pack())
        for entry in entries:
            with open(entry.path, 'rb') as fr:
                data = fr.read()
            fw.write(data)


# core logic
if __name__ == "__main__":
    try:
        check_all_tools_intact()
        print(messages[0])
        press_any_key()
        pack_from_xlsx_to_cst_files()
        pack_from_ini_to_cstl_files()
        pack_int_archive()

    except Exception as error:
        print("ERROR - " + str("".join(traceback.format_exception(type(error),
                                                                  value=error,
                                                                  tb=error.__traceback__))).split(
            "The above exception was the direct cause of the following")[0])
    finally:
        print(messages[1])
