import pandas as pd

import struct
import zlib
from sys import executable
from codecs import open as copen
from os import path, mkdir, chmod, rename, chdir, listdir, remove, scandir, rmdir
from shutil import copy, move
from traceback import format_exception
from colorama import init, Fore
from subprocess import call, DEVNULL
from pandas import DataFrame, ExcelWriter, read_csv

init(autoreset=True)

game_main = "None"

messages = ["""CatSystem2 Simple tools (extraction tool) by ShereKhanRomeo\n
HUGE thanks to Trigger-Segfault for explaining and tool links\n
Following game files are MANDATORY to be in the folder with this unpacker:\n
0) main game executable   (found successfully)
1) config.int = needed for 'nametable.csv' in it
2) scene.int  = contains all story's text scripts\n
optional files, if game has any of those:
3) update00.int\n4) update01.int and all other 'updateXX.int' files

Files in each 'updateXX.int' archive overwrite according files from other int-archives,
including files from 'updateXX.int' archives with lesser number, so you better copy here all update-files.
Thus, this unpacker extracts mandatory archives first and then overrides extracted files with ones
unpacked from 'updateXX' archives.

Current version automatically unpacks and prepares for translation .cst and cstl-scripts with texts and 'nametable.csv'.
Other kinds of files to translate game menu, images or videos will be extracted, but not processed automatically.

After copying all files into this folder press Enter...""",

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
dir_path = path.dirname(path.realpath(__file__)).replace("tools", "")
print("Path: " + dir_path)
dir_path_tools = dir_path + "tools\\"
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

hgx2bmp_exe = "hgx2bmp.exe"
zlib1_dll = "zlib1.dll"
exzt_exe = "exzt.exe"
exkifint_v3_exe = "exkifint_v3.exe"
cs2_decompile_exe = "cs2_decompile.exe"
cstl_tool_zip = "cstl_tool.zip"

# i am ignoring kx2.ini archive for now, since i have no idea about .kx2-files it has inside
temp_archives = ["scene.int", "fes.int", "config.int", "update00.int", "update01.int", "update02.int", "update03.int",
                 "update04.int", "update05.int", "update06.int", "update07.int", "update08.int", "update09.int",
                 "update10.int", "update11.int", "update12.int", "update13.int", "update14.int", "update15.int"]
temp_tools = [hgx2bmp_exe, zlib1_dll, exzt_exe, exkifint_v3_exe, cs2_decompile_exe, cstl_tool_zip]
optional_voice_packages = []


# functions
def press_any_key():
    input()


def create_if_not_exists(_path_to_file_or_dir: str):
    if not path.exists(_path_to_file_or_dir):
        mkdir(_path_to_file_or_dir)


def prepare_for_work():
    global optional_voice_packages
    import string
    template = "pcm_{0}.int"
    for letter in string.ascii_letters:
        optional_voice_packages.append(str.format(template, letter))
    create_if_not_exists(dir_path_extracted)
    create_if_not_exists(dir_path_extracted_manually)
    create_if_not_exists(dir_path_extracted_animations)
    create_if_not_exists(dir_path_extracted_images)
    create_if_not_exists(dir_path_extracted_movies)
    create_if_not_exists(dir_path_extracted_scripts)
    create_if_not_exists(dir_path_extracted_sounds)
    create_if_not_exists(dir_path_extracted_texts)
    create_if_not_exists(dir_path_extracted_localization_texts)
    create_if_not_exists(dir_path_translate_here)
    create_if_not_exists(dir_path_translate_here_clean_texts)
    create_if_not_exists(dir_path_translate_here_clean_localization_texts)
    create_if_not_exists(dir_path_translate_here_other_files)
    create_if_not_exists(dir_path_translate_here_other_files_images)
    create_if_not_exists(dir_path_translate_here_other_files_movies)
    create_if_not_exists(dir_path_translate_here_other_files_sounds)
    create_if_not_exists(dir_path_translate_here_other_files_other)


def check_all_tools_intact():
    global game_main, temp_tools
    dir_path_cs2_bin = dir_path + "\\cs2.bin"
    if path.exists(dir_path_cs2_bin):
        chmod(dir_path_cs2_bin, 0o777)
        chmod(dir_path + "\\cs2.exe", 0o777)
        rename(dir_path + "\\cs2.exe", dir_path + "\\сs2.bin")  # rename into cs2.bin where C is russian XD
        rename(dir_path_cs2_bin, dir_path + "\\cs2.exe")

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

    missing_files = ""
    for tool in temp_tools:
        if not path.exists(dir_path_tools + tool):
            missing_files += tool + " "
    if len(missing_files) > 0:
        print(str.format(messages[7], missing_files))
        press_any_key()
        exit(0)
    temp_tools.append(game_main)


def copy_files_into_extract_folder_and_extract():
    global game_main
    copy(dir_path + "\\" + game_main, dir_path_extracted + game_main)
    copy(dir_path_tools + exkifint_v3_exe, dir_path_extracted + exkifint_v3_exe)
    for file in temp_archives:
        if path.exists(dir_path + "\\" + file):
            print(str.format(messages[2], file))
            copy(dir_path + "\\" + file, dir_path_extracted + file)
    print(messages[1])
    chdir(dir_path_extracted)
    # unpacking from int archives
    if path.exists(dir_path_extracted + exkifint_v3_exe) and path.exists(dir_path_extracted + game_main):
        for archive in listdir(dir_path_extracted):
            if archive in temp_archives:
                print(str.format(messages[3], archive))
                call([exkifint_v3_exe, archive, game_main], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted, ".int")
    delete_file(dir_path_extracted + exkifint_v3_exe)
    chdir(dir_path)


def sort_resulting_files():
    print(messages[5])
    chdir(dir_path_extracted)

    for filename in listdir(dir_path_extracted):
        file = dir_path_extracted + filename
        if path.isfile(file):
            if file.endswith(".anm"):
                move(file, dir_path_extracted_animations + filename)
            if file.endswith(".hg2") or file.endswith(".hg3") or file.endswith(".bmp") or file.endswith(".jpg"):
                move(file, dir_path_extracted_images + filename)
            if file.endswith(".mpg"):
                move(file, dir_path_extracted_movies + filename)
            if file.endswith(".fes") or file.endswith(".kcs") or file.endswith(".dat") or file.endswith(".xml"):
                move(file, dir_path_extracted_scripts + filename)
            if file.endswith(".ogg") or file.endswith(".wav"):
                move(file, dir_path_extracted_sounds + filename)
            if file.endswith(".cst") or file.endswith(".txt"):
                move(file, dir_path_extracted_texts + filename)
            if file.endswith(".cstl"):
                move(file, dir_path_extracted_localization_texts + filename)
    chdir(dir_path)


def process_nametable():
    chdir(dir_path_extracted)
    nametable_csv = dir_path_extracted + 'nametable.csv'
    nametable_xlsx = dir_path_translate_here + 'nametable.xlsx'
    if not path.exists(nametable_csv) or not path.isfile(nametable_csv):
        print("\nFile 'nametable.csv' was not found during unpacking.\n"
              "Step '2) apply name translations' will not be functional.\n"
              "Translate all names in text files manually.\n")
        press_any_key()
    else:
        # if nametable.csv exists
        text_names = []
        translates_to = []
        write_name_here = []
        translated_names = False
        if path.exists(nametable_xlsx) and path.isfile(nametable_xlsx):
            # if it exists - save translations column from it
            xlsx_file = pd.ExcelFile(nametable_xlsx, engine='openpyxl')
            df1 = xlsx_file.parse(xlsx_file.sheet_names[0])
            write_name_here = list(df1[df1.columns[2]]).copy()
            translated_names = True
        df0 = None
        encodings = ["ShiftJIS", "utf-8"]
        for encoding in encodings:
            try:
                df0 = read_csv(nametable_csv, encoding=encoding)
            except UnicodeDecodeError:
                pass
            else:
                break

        if df0 is not None:
            # we need to process first line of CSV separately,
            # since lib thinks it's "table headers" while it might be not, it might be data right away
            if '\t' in df0.columns[0]:
                text_names.append(df0.columns[0].split('\t')[1].replace("\\fs　\\fn", " "))
                translates_to.append("will be translated as:")
                if not translated_names:
                    write_name_here.append("(translate name here)")
            # processing other CSV lines
            for line in list(df0.values):
                if '\t' in line[0]:
                    name = line[0].split('\t')[1].strip("【】").replace("\\fs　\\fn", " ")
                    if name not in text_names:
                        text_names.append(name)
                        translates_to.append("will be translated as:")
                        if not translated_names:
                            write_name_here.append("(translate name here)")
            df = DataFrame({"Names": text_names, "will be shown as": translates_to, "New names:": write_name_here})
            writer = ExcelWriter(nametable_xlsx, engine='xlsxwriter')
            pd.set_option('display.max_colwidth', None)
            df.to_excel(writer, sheet_name='sheetName', index=False, na_rep='NaN')
            writer.sheets['sheetName'].set_column(0, 0, 20)
            writer.sheets['sheetName'].set_column(1, 1, 20)
            writer.sheets['sheetName'].set_column(2, 2, 20)
            writer.close()
        else:
            print("Can not understand encoding of 'nametable.csv'.\n"
                  "Step '2) apply name translations' will not be functional.\n"
                  "Translate all names in text files manually.")
    chdir(dir_path)


def extract_zt_archives():
    chdir(dir_path_extracted)
    copy(dir_path_tools + exzt_exe, dir_path_extracted + exzt_exe)
    copy(dir_path_tools + zlib1_dll, dir_path_extracted + zlib1_dll)
    # unpacking from int archives
    if path.exists(dir_path_extracted + exzt_exe) \
            and path.exists(dir_path_extracted + zlib1_dll):
        for archive in listdir(dir_path_extracted):
            if archive.endswith(".zt"):
                archive_ini = dir_path_extracted + archive
                if path.exists(archive_ini):
                    print(str.format(messages[3], archive))
                    call([exzt_exe, archive], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted, ".zt")
    delete_file(dir_path_extracted + exzt_exe)
    delete_file(dir_path_extracted + zlib1_dll)
    chdir(dir_path)


def unpack_scripts():
    chdir(dir_path_extracted_scripts)
    copy(dir_path_tools + cs2_decompile_exe, dir_path_extracted_scripts + cs2_decompile_exe)
    if path.exists(dir_path_extracted_scripts + cs2_decompile_exe):
        for filename in listdir(dir_path_extracted_scripts):
            file = dir_path_extracted_scripts + filename
            if file.endswith(".fes"):
                print(str.format(messages[3], filename))
                call([cs2_decompile_exe, filename], stdin=None, stdout=None, stderr=None, shell=False)
    delete_file(dir_path_extracted_scripts + cs2_decompile_exe)
    chdir(dir_path)


def unpack_images():
    chdir(dir_path_extracted_images)
    # unpacking .hg2 and .hg3 files to .bmp files
    copy(dir_path_tools + hgx2bmp_exe, dir_path_extracted_images + hgx2bmp_exe)
    copy(dir_path_tools + zlib1_dll, dir_path_extracted_images + zlib1_dll)
    if path.exists(dir_path_extracted_images + hgx2bmp_exe):
        for filename in listdir(dir_path_extracted_images):
            file = dir_path_extracted_images + filename
            if file.endswith(".hg2") or file.endswith(".hg3"):
                print(str.format(messages[3], filename))
                call([hgx2bmp_exe, filename], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted_images, ".hg2")
    clean_files_from_dir(dir_path_extracted_images, ".hg3")
    delete_file(dir_path_extracted_images + hgx2bmp_exe)
    delete_file(dir_path_extracted_images + zlib1_dll)
    chdir(dir_path)

def excst(f):
    fs = open(f, 'rb')
    fs.seek(8)
    raw_size, ori_size = struct.unpack('II',fs.read(8))
    raw=fs.read()
    if len(raw)!=raw_size:
        raise Exception('size error! ' + str(len(raw)) + " | " + str(raw_size) + " | " + str(ori_size))
    ori=zlib.decompress(raw)
    if len(ori)!=ori_size:
        raise Exception('size error2! ' + str(len(ori)) + " | " + str(ori_size))
    fs.close()
    fs1 = open(f.replace('.cst', '.txt'), 'wb')
    fs1.write(ori)
    fs1.close()


def unpack_texts():
    chdir(dir_path_extracted_texts)
    # unpacking .cst files to .out files
    copy(dir_path_tools + cs2_decompile_exe, dir_path_extracted_texts + cs2_decompile_exe)
    if path.exists(dir_path_extracted_texts + cs2_decompile_exe):
        for filename in listdir(dir_path_extracted_texts):
            file = dir_path_extracted_texts + filename
            if file.endswith(".cst"):
                call([cs2_decompile_exe, filename], stdin=None, stdout=None, stderr=None, shell=False)
    delete_file(dir_path_extracted_texts + cs2_decompile_exe)
    # extracting text lines from .txt files into .xlsx files
    extract_clean_text()
    chdir(dir_path)


def extract_clean_text():
    problematic_files = []

    for filename in listdir(dir_path_extracted_texts):
        if path.isfile(filename) and filename.endswith(".txt"):
            full_filename_txt = dir_path_extracted_texts + filename
            print(str.format(messages[3], filename))
            encoding = "ShiftJIS"
            if game_main == "ISLAND.exe":
                encoding = "ANSI"
            file_lines = []
            text_lines = []
            try:
                with copen(full_filename_txt, mode="rb", encoding=encoding) as file:
                    file_lines = file.readlines()
                    file.close()
            except UnicodeDecodeError as err:
                problematic_files.append(filename)
                continue
            for line in file_lines[1:]:
                if (line.endswith(TEXT_LINE_END1)
                        or line.endswith(TEXT_LINE_END2)
                        or ("[" in line
                            and "]" in line
                            and not line.startswith("\tbg")
                            and not line.startswith("\tcg")
                            and not line.startswith("\teg")
                            and not line.startswith("\tfg")
                            and not line.startswith("\tpl")
                            and not line.startswith("\tpr"))
                        or line.startswith(SCENE_LINESTART1)
                        or line.startswith(SCENE_LINESTART2)
                        or line.startswith(SCENE_LINESTART3)):
                    if "\\r\\fn" not in line and not line == '\t\\fn\r\n':
                        # text lines we need for translation
                        text_lines.append(line)
            column1_ids = []
            column2_names = []
            column3_lines = []
            column3_lines_old = []
            file_xlsx = dir_path_translate_here_clean_texts + filename.replace(".txt", ".xlsx")
            if path.exists(file_xlsx) and path.isfile(file_xlsx):
                # if it exists - save translations column from it
                xlsx_file = pd.ExcelFile(file_xlsx, engine='openpyxl')
                df0 = xlsx_file.parse(xlsx_file.sheet_names[0])
                column3_lines_old = list(df0[df0.columns[2]]).copy()
            for i in range(len(text_lines)):
                current_line = text_lines[i]
                if (current_line.endswith(TEXT_LINE_END1)
                        or current_line.endswith(TEXT_LINE_END2)
                        or ("[" in current_line
                            and "]" in current_line
                            and not current_line.startswith("\tbg")
                            and not current_line.startswith("\tcg")
                            and not current_line.startswith("\teg")
                            and not current_line.startswith("\tfg")
                            and not current_line.startswith("\tpl")
                            and not current_line.startswith("\tpr"))):
                    # if it's usual text line
                    text_line_parts = current_line.split("\t")
                    if len(text_line_parts) == 2:
                        character_name = text_line_parts[0]
                        if len(character_name) == 0:
                            character_name = EMPTY_CHARACTER_NAME
                        column2_names.append(character_name)
                        column2_names.append(character_name)
                        text_line = text_line_parts[1]
                        # we need to remove "@" if present,
                        # but only if it's at the end of the line, not to remove "@" from inside the main text
                        column3_lines.append(text_line
                                             .replace(TEXT_LINE_END2, "")
                                             .replace("\r\n", "")
                                             .replace("\\fn", "")
                                             .replace("\\fl", "")
                                             .replace("\\fs", "")
                                             .replace("\\pc", "")
                                             .replace("\\pl", "")
                                             .replace("[", "")
                                             .replace("]", ""))
                        if len(column3_lines_old) > 1:
                            column3_lines_old.pop(0)
                            column3_lines.append(column3_lines_old.pop(0))
                        else:
                            column3_lines.append(WRITE_TRANSLATION_HERE)
                        column1_ids.append(str.format(ORIGINAL_LINE_PATTERN, i))
                        column1_ids.append(str.format(TRANSLATION_LINE_PATTERN, i))
                    else:
                        raise Exception("\n\n!!ERROR!!\n"
                                        "There are lines with more that one TAB symbol in 1 line!\n"
                                        "This is unexpected... "
                                        + "Please, contact developer on github with screenshot of this line:\n "
                                        + str(current_line.encode(encoding=encoding)) + "\n")

                elif (current_line.startswith(SCENE_LINESTART1)
                      or current_line.startswith(SCENE_LINESTART2)
                      or current_line.startswith(SCENE_LINESTART3)):
                    # if it's scene title (naming)
                    column2_names.append(SCENE_TITLE)
                    column2_names.append(SCENE_TITLE)
                    column3_lines.append(current_line
                                         .replace(SCENE_LINESTART1, "")
                                         .replace(SCENE_LINESTART2, "")
                                         .replace(SCENE_LINESTART3, "")
                                         .replace("\r\n", ""))
                    if len(column3_lines_old) > 1:
                        column3_lines_old.pop(0)
                        column3_lines.append(column3_lines_old.pop(0))
                    else:
                        column3_lines.append(WRITE_TRANSLATION_HERE)
                    column1_ids.append(str.format(ORIGINAL_LINE_PATTERN, i))
                    column1_ids.append(str.format(TRANSLATION_LINE_PATTERN, i))
            if len(column1_ids) > 0 and len(column2_names) > 0 and len(column3_lines) > 0:
                df = DataFrame({"Lines numbers": column1_ids,
                                "Character name": column2_names,
                                "Line text": column3_lines})
                writer = ExcelWriter(file_xlsx, engine='xlsxwriter')
                df.to_excel(writer, sheet_name='sheetName', index=False, na_rep='NaN')
                writer.sheets['sheetName'].set_column(0, 0, 20)
                writer.sheets['sheetName'].set_column(1, 1, 15)
                writer.sheets['sheetName'].set_column(2, 2, 110)
                writer.close()
    if len(problematic_files) > 0:
        print(Fore.RED + "There were problems with reading these files:\n" + '\n'.join(problematic_files))


def extract_localized_texts():
    foundLocFiles = False

    # for filename in listdir(dir_path_extracted_texts):
    #     if filename.endswith(".cst"):
    #         foundLocFiles = True
    #         print(str.format(messages[3], filename))
    #         call([
    #             executable,
    #             dir_path_tools + cstl_tool_zip,
    #             "-b", dir_path_extracted_texts + filename,
    #             "-t", "cstl",
    #             "-o", dir_path_extracted_localization_texts + filename.replace(".cst", ".cstl"),
    #             "--orig-lang", "en"
    #         ], stdin=None, stdout=DEVNULL, stderr=None, shell=False)

    for filename in listdir(dir_path_extracted_localization_texts):
        if filename.endswith(".cstl"):
            foundLocFiles = True
            print(str.format(messages[3], filename))
            call([
                executable,
                dir_path_tools + cstl_tool_zip,
                "-d", dir_path_extracted_localization_texts + filename,
                "-o", dir_path_translate_here_clean_localization_texts + filename.replace(".cstl", ".ini")
            ], stdin=None, stdout=DEVNULL, stderr=None, shell=False)
    if foundLocFiles:
        print(Fore.YELLOW + "\nGame has localization files! Please translate using them and not via Excel tables.")


def remove_temp_files():
    print(messages[4])
    for file in temp_archives:
        delete_file(dir_path_extracted + file)
    for file in temp_tools:
        delete_file(dir_path_extracted + file)


def delete_file(path_to_file: str):
    if path.exists(path_to_file):
        chmod(path_to_file, 0o777)
        remove(path_to_file)


def remove_empty_folders():
    # also remove empty folders
    if path.exists(dir_path_extracted_manually):
        for pth in listdir(dir_path_extracted_manually):
            if path.isdir(dir_path_extracted_manually + pth):
                with scandir(dir_path_extracted_manually + pth) as it:
                    if not any(it):
                        rmdir(dir_path_extracted_manually + pth)


def clean_files_from_dir(_dir: str, _filetype: str):
    for filename in listdir(_dir):
        file = _dir + filename
        if file.endswith(_filetype):
            delete_file(file)


# core logic
try:
    check_all_tools_intact()
    print(messages[0])
    press_any_key()
    prepare_for_work()
    copy_files_into_extract_folder_and_extract()
    sort_resulting_files()
    process_nametable()

    unpack_texts()
    extract_localized_texts()
    unpack_scripts()
    #unpack_images()

except Exception as error:
    print("ERROR - " + str("".join(format_exception(type(error), value=error, tb=error.__traceback__))).split(
        "The above exception was the direct cause of the following")[0])
finally:
    remove_temp_files()
    remove_empty_folders()
    print(messages[6])  # done
