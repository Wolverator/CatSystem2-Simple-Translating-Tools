import codecs
import os
import shutil
import sys
import traceback

import pandas
from colorama import init, Fore
from subprocess import call
from pandas import DataFrame, ExcelWriter

init(autoreset=True)

messages = ["""CatSystem2 Simple tools (extraction tool) by ShereKhanRomeo\n
HUGE thanks to Trigger-Segfault for explaining and tool links
check his wiki here https://github.com/trigger-segfault/TriggersTools.CatSystem2/wiki \n\n
Following game files are MANDATORY to be copied into folder with this unpacker:\n
0) cs2.exe      = main file of your game, it's usually 4 to 5 MB (copy here and rename into 'cs2')
   or cs2.bin   = if your game's .exe is less than 1MB - copy .bin file instead (it still should be 4 to 5 MB)
1) config.int = needed for 'nametable.csv' in it
2) scene.int  = contains all story's text scripts\n
optional files, if game has any of those:
3) update00.int\n4) update01.int and all other 'updateXX.int' files

Files in each 'updateXX.int' archive overwrite according files from other int-archives,
including files from 'updateXX.int' archives with lesser number, so you better copy here all update-files.
Thus, this unpacker extracts mandatory archives first and then overrides extracted files with ones
unpacked from 'updateXX' archives.

Current version automatically unpacks and prepares for translation only cst-scripts with texts and 'nametable.csv'.
Other kinds of files to translate game menu, images or videos will be extracted, but not processed automatically.

IMPORTANT! While translating, be sure to check if all scripts of '.cst' files are correct.
(visible in according '.txt' files)
Detailed help for .cst commands can be found on GitHub page of this unpacker.

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
dir_path = os.path.dirname(os.path.realpath(__file__)).replace("tools", "")
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

TRANSLATION_LINE_PATTERN = "translation for line #{0}"
ORIGINAL_LINE_PATTERN = "original line #{0}"
TEXT_LINE_END1 = "\\fn\r\n"
TEXT_LINE_END2 = "\\@\r\n"
SCENE_LINESTART1 = "\tscene "
SCENE_LINESTART2 = "\tstr 3 " # for Grisaia1 steam version
SCENE_LINESTART3 = "\tstr 155 " # for Grisaia1 unrated version
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


# functions
def press_any_key():
    skip = input()


def create_if_not_exists(_path_to_file_or_dir: str):
    if not os.path.exists(_path_to_file_or_dir):
        os.mkdir(_path_to_file_or_dir)


def prepare_for_work():
    global optional_voice_packages
    import string
    template = "pcm_{0}.int"
    for letter in string.ascii_lowercase:
        optional_voice_packages.append(str.format(template, letter))
    create_if_not_exists(dir_path_extracted)
    create_if_not_exists(dir_path_extracted_manually)
    create_if_not_exists(dir_path_extracted_animations)
    create_if_not_exists(dir_path_extracted_images)
    create_if_not_exists(dir_path_extracted_movies)
    create_if_not_exists(dir_path_extracted_scripts)
    create_if_not_exists(dir_path_extracted_sounds)
    create_if_not_exists(dir_path_extracted_texts)
    create_if_not_exists(dir_path_translations)
    create_if_not_exists(dir_path_translations_clean_texts)
    create_if_not_exists(dir_path_translations_other_files)
    create_if_not_exists(dir_path_translations_other_files_images)
    create_if_not_exists(dir_path_translations_other_files_movies)
    create_if_not_exists(dir_path_translations_other_files_sounds)
    create_if_not_exists(dir_path_translations_other_files_other)


def check_all_tools_intact():
    missing_files = ""
    for tool in temp_tools:
        if not os.path.exists(dir_path_tools + tool):
            missing_files += tool + " "
    if len(missing_files) > 0:
        print(str.format(messages[7], missing_files))
        press_any_key()
        sys.exit(0)


def copy_files_into_extract_folder():
    global game_main
    print(messages[1])
    dir_path_cs2_bin = dir_path + "\\cs2.bin"
    # TODO make unpacker check for correct file with VCODEs not to make user rename files
    if os.path.exists(dir_path_cs2_bin):
        os.chmod(dir_path_cs2_bin, 0o777)
        os.rename(dir_path_cs2_bin, dir_path + "\\cs2.exe")

    for file in temp_files:
        if os.path.exists(dir_path + "\\" + file):
            print(str.format(messages[2], file))
            shutil.copy(dir_path + "\\" + file, dir_path_extracted + file)


def extract_int_archives():
    os.chdir(dir_path_extracted)
    shutil.copy(dir_path_tools + exkifint_v3_exe, dir_path_extracted + exkifint_v3_exe)
    # unpacking from int archives
    if os.path.exists(dir_path_extracted + exkifint_v3_exe) \
            and os.path.exists(dir_path_extracted + game_main):
        for archive in temp_archives:
            archive_ini = dir_path_extracted + archive
            if os.path.exists(archive_ini):
                print(str.format(messages[3], archive))
                call([exkifint_v3_exe, archive, game_main], stdin=None, stdout=None, stderr=None, shell=False)
        for archive in optional_voice_packages:
            archive_ini = dir_path_extracted + archive
            if os.path.exists(archive_ini):
                print(str.format(messages[3], archive))
                call([exkifint_v3_exe, archive, game_main], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted, ".int")
    delete_file(dir_path_extracted + exkifint_v3_exe)
    os.chdir(dir_path)


def extract_zt_archives():
    os.chdir(dir_path_extracted)
    shutil.copy(dir_path_tools + exzt_exe, dir_path_extracted + exzt_exe)
    shutil.copy(dir_path_tools + zlib1_dll, dir_path_extracted + zlib1_dll)
    # unpacking from int archives
    if os.path.exists(dir_path_extracted + exzt_exe) \
            and os.path.exists(dir_path_extracted + zlib1_dll):
        for archive in os.listdir(dir_path_extracted):
            if archive.endswith(".zt"):
                archive_ini = dir_path_extracted + archive
                if os.path.exists(archive_ini):
                    print(str.format(messages[3], archive))
                    call([exzt_exe, archive], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted, ".zt")
    delete_file(dir_path_extracted + exzt_exe)
    delete_file(dir_path_extracted + zlib1_dll)
    os.chdir(dir_path)


def unpack_scripts():
    os.chdir(dir_path_extracted_scripts)
    shutil.copy(dir_path_tools + cs2_decompile_exe, dir_path_extracted_scripts + cs2_decompile_exe)
    if os.path.exists(dir_path_extracted_scripts + cs2_decompile_exe):
        for filename in os.listdir(dir_path_extracted_scripts):
            file = dir_path_extracted_scripts + filename
            if file.endswith(".kcs") or file.endswith(".fes"):
                print(str.format(messages[3], filename))
                call([cs2_decompile_exe, filename], stdin=None, stdout=None, stderr=None, shell=False)
    delete_file(dir_path_extracted_scripts + cs2_decompile_exe)
    os.chdir(dir_path)


def unpack_images():
    os.chdir(dir_path_extracted_images)
    # unpacking .hg2 and .hg3 files to .bmp files
    shutil.copy(dir_path_tools + hgx2bmp_exe, dir_path_extracted_images + hgx2bmp_exe)
    shutil.copy(dir_path_tools + zlib1_dll, dir_path_extracted_images + zlib1_dll)
    if os.path.exists(dir_path_extracted_images + hgx2bmp_exe):
        for filename in os.listdir(dir_path_extracted_images):
            file = dir_path_extracted_images + filename
            if file.endswith(".hg2") or file.endswith(".hg3"):
                print(str.format(messages[3], filename))
                call([hgx2bmp_exe, filename], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted_images, ".hg2")
    clean_files_from_dir(dir_path_extracted_images, ".hg3")
    delete_file(dir_path_extracted_images + hgx2bmp_exe)
    delete_file(dir_path_extracted_images + zlib1_dll)
    os.chdir(dir_path)


def unpack_texts():
    os.chdir(dir_path_extracted_texts)
    # unpacking .cst files to .out files
    shutil.copy(dir_path_tools + cs2_decompile_exe, dir_path_extracted_texts + cs2_decompile_exe)
    if os.path.exists(dir_path_extracted_texts + cs2_decompile_exe):
        for filename in os.listdir(dir_path_extracted_texts):
            file = dir_path_extracted_texts + filename
            if file.endswith(".cst"):
                print(str.format(messages[3], filename))
                call([cs2_decompile_exe, filename], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted_texts, ".cst")
    delete_file(dir_path_extracted_texts + cs2_decompile_exe)

    # extracting text lines from .txt files into .xlsx files
    extract_clean_text()
    os.chdir(dir_path)


def extract_clean_text():
    for filename in os.listdir(dir_path_extracted_texts):
        if os.path.isfile(filename) and filename.endswith(".txt"):
            full_filename_txt = dir_path_extracted_texts + filename
            print(str.format(messages[3], filename))
            encodingShiftJIS = "ShiftJIS"
            file_lines = []
            text_lines = []
            try:
                with codecs.open(full_filename_txt, mode="rb", encoding=encodingShiftJIS) as file:
                    file_lines = file.readlines()
                    file.close()
            except UnicodeDecodeError as err:
                continue
            for line in file_lines[1:]:
                if line.endswith(TEXT_LINE_END1) or line.endswith(TEXT_LINE_END2)\
                        or line.startswith(SCENE_LINESTART1) or line.startswith(SCENE_LINESTART2) or line.startswith(SCENE_LINESTART3):
                    if "\\r\\fn" not in line and not line == '\t\\fn\r\n':
                        # text lines we need for translation
                        text_lines.append(line)

            column1_ids = []
            column2_names = []
            column3_lines = []
            column3_lines_old = []

            file_xlsx = dir_path_translations_clean_texts + filename.replace(".txt", ".xlsx")

            if os.path.exists(file_xlsx) and os.path.isfile(file_xlsx):
                # if it exists - save translations column from it
                xlsx_file = pandas.ExcelFile(file_xlsx)
                df0 = xlsx_file.parse(xlsx_file.sheet_names[0])
                column3_lines_old = list(df0[df0.columns[2]]).copy()

            for i in range(len(text_lines)):
                current_line = text_lines[i]
                if current_line.endswith(TEXT_LINE_END1) or current_line.endswith(TEXT_LINE_END2):
                    # if it's usual text line
                    text_line_parts = text_lines[i].split("\t")
                    if len(text_line_parts) == 2:
                        character_name = text_line_parts[0]
                        if len(character_name) == 0:
                            character_name = EMPTY_CHARACTER_NAME
                        column2_names.append(character_name)
                        column2_names.append(character_name)

                        text_line = text_line_parts[1]
                        # we need to remove "@" if present, but only if it's at the end of the line, not to remove "@" from inside the main text
                        column3_lines.append(text_line.replace(TEXT_LINE_END2, "").replace("\r\n", "").replace("\\fn", ""))
                        if len(column3_lines_old) > 1:
                            column3_lines_old.pop(0)
                            column3_lines.append(column3_lines_old.pop(0))
                        else:
                            column3_lines.append(WRITE_TRANSLATION_HERE)
                        column1_ids.append(str.format(ORIGINAL_LINE_PATTERN, i))
                        column1_ids.append(str.format(TRANSLATION_LINE_PATTERN, i))
                    else:
                        raise Exception("\n\n!!ERROR!!\nThere are lines with more that one TAB symbol in 1 line!\nThis is unexpected... "
                                        + "Please, contact developer on github with screenshot of this line:\n "
                                        + str(current_line.encode(encoding=encodingShiftJIS)) + "\n")

                elif current_line.startswith(SCENE_LINESTART1) or current_line.startswith(SCENE_LINESTART2) or current_line.startswith(SCENE_LINESTART3):
                    # if it's scene title (naming)
                    column2_names.append(SCENE_TITLE)
                    column2_names.append(SCENE_TITLE)
                    column3_lines.append(current_line.replace(SCENE_LINESTART1, "").replace(SCENE_LINESTART2, "").replace(SCENE_LINESTART3, "").replace("\r\n", ""))
                    if len(column3_lines_old) > 1:
                        column3_lines_old.pop(0)
                        column3_lines.append(column3_lines_old.pop(0))
                    else:
                        column3_lines.append(WRITE_TRANSLATION_HERE)
                    column1_ids.append(str.format(ORIGINAL_LINE_PATTERN, i))
                    column1_ids.append(str.format(TRANSLATION_LINE_PATTERN, i))


            if len(column1_ids) > 0 and len(column2_names) > 0 and len(column3_lines) > 0:
                df = DataFrame({"Lines numbers": column1_ids, "Character name": column2_names, "Line text": column3_lines})
                writer = ExcelWriter(file_xlsx)
                df.to_excel(writer, sheet_name='sheetName', index=False, na_rep='NaN')
                for column in df:
                    column_length = max(df[column].astype(str).map(len).max(), len(column))
                    col_idx = df.columns.get_loc(column)
                    writer.sheets['sheetName'].set_column(col_idx, col_idx, column_length)
                writer.save()


def sort_resulting_files():
    print(messages[5])
    os.chdir(dir_path_extracted)

    for filename in os.listdir(dir_path_extracted):
        file = dir_path_extracted + filename
        if os.path.isfile(file):
            if file.endswith(".anm"):
                shutil.move(file, dir_path_extracted_animations + filename)
            if file.endswith(".hg2") or file.endswith(".hg3") or file.endswith(".bmp") or file.endswith(".jpg"):
                shutil.move(file, dir_path_extracted_images + filename)
            if file.endswith(".mpg"):
                shutil.move(file, dir_path_extracted_movies + filename)
            if file.endswith(".fes") or file.endswith(".kcs") or file.endswith(".dat") or file.endswith(".xml") or file.endswith(".txt"):
                shutil.move(file, dir_path_extracted_scripts + filename)
            if file.endswith(".ogg") or file.endswith(".wav"):
                shutil.move(file, dir_path_extracted_sounds + filename)
            if file.endswith(".cst"):
                shutil.move(file, dir_path_extracted_texts + filename)

    nametable_csv = dir_path_extracted + 'nametable.csv'
    nametable_xlsx = dir_path_translations + 'nametable.xlsx'
    if not os.path.exists(nametable_csv) or not os.path.isfile(nametable_csv):
        for pth in os.listdir(dir_path_translations):
            if os.path.isdir(dir_path_translations + pth):
                with os.scandir(dir_path_translations + pth) as it:
                    if not any(it):
                        os.rmdir(dir_path_translations + pth)
        os.rmdir(dir_path_translations[:-1])
        print(messages[8])  # nametable not found
        press_any_key()
        sys.exit(0)
    else:
        # if nametable.csv exists
        text_names = []
        translates_to = []
        write_name_here = []
        translated_names = False
        if os.path.exists(nametable_xlsx) and os.path.isfile(nametable_xlsx):
            #if it exists - save translations column from it
            xlsx_file = pandas.ExcelFile(nametable_xlsx)
            df1 = xlsx_file.parse(xlsx_file.sheet_names[0])
            write_name_here = list(df1[df1.columns[2]]).copy()
            translated_names = True
        df0 = pandas.read_csv(nametable_csv, encoding='ShiftJIS')
        text_names.append(df0.columns[0].split('\t')[1].replace("\\fs　\\fn", " "))
        translates_to.append("will be translated as:")
        if not translated_names:
            write_name_here.append("(translate name here)")
        for line in df0.values.tolist():
            name = line[0].split('\t')[1].strip("【】").replace("\\fs　\\fn", " ")
            if name not in text_names:
                text_names.append(name)
                translates_to.append("will be translated as:")
                if not translated_names:
                    write_name_here.append("(translate name here)")
        df = DataFrame({"Names": text_names, "will be shown as": translates_to, "New names:": write_name_here})
        writer = ExcelWriter(nametable_xlsx)
        df.to_excel(writer, sheet_name='sheetName', index=False, na_rep='NaN')
        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['sheetName'].set_column(col_idx, col_idx, column_length)
        writer.save()
    os.chdir(dir_path)


def remove_temp_files():
    print(messages[4])
    for file in temp_files:
        delete_file(dir_path_extracted + file)
    for file in temp_tools:
        delete_file(dir_path_extracted + file)


def delete_file(path_to_file: str):
    if os.path.exists(path_to_file):
        os.chmod(path_to_file, 0o777)
        os.remove(path_to_file)


def remove_empty_folders():
    # also remove empty folders
    for pth in os.listdir(dir_path_extracted_manually):
        if os.path.isdir(dir_path_extracted_manually + pth):
            with os.scandir(dir_path_extracted_manually + pth) as it:
                if not any(it):
                    os.rmdir(dir_path_extracted_manually + pth)


def clean_files_from_dir(_dir: str, _filetype: str):
    for filename in os.listdir(_dir):
        file = _dir + filename
        if file.endswith(_filetype):
            delete_file(file)


# core logic
try:
    check_all_tools_intact()
    print(messages[0])
    press_any_key()
    prepare_for_work()
    copy_files_into_extract_folder()
    extract_int_archives()
    sort_resulting_files()

    unpack_texts()

except Exception as error:
    print("ERROR - " + str("".join(traceback.format_exception(type(error), value=error, tb=error.__traceback__))).split(
        "The above exception was the direct cause of the following")[0])
finally:
    remove_temp_files()
    remove_empty_folders()
    print(messages[6])  # done
