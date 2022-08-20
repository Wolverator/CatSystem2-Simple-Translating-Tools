import codecs
import ctypes
import locale
import os
import shutil
import sys
import traceback
from subprocess import call

from pandas import DataFrame

# locales to help more enthusiasts understand this tool
# just create new list with your translation and insert it into "select_locale()"
# locale[0] = intro
# locale[1] = copying files
# locale[2] = copying file
# locale[3] = unpacking
# locale[4] = removing temp files
# locale[5] = sorting files
# locale[6] = done! Enter to exit
# locale[7] = error missing files, Enter to exit
TRANSLATION_LINE_PATTERN = "translation for line #{0}"
ORIGINAL_LINE_PATTERN = "original line #{0}"
TEXT_LINE_END1 = "\\fn\r\n"
TEXT_LINE_END2 = "@\r\n"
SCENE_LINESTART1 = "\tscene "
SCENE_LINESTART2 = "\tstr 155 "
WRITE_TRANSLATION_HERE = "(write translation here)"
CHOICE_OPTION = "choice_option"
SCENE_TITLE = "scene_title"

locale_to_use = []
locale_ru = ["""Распаковщик ресурсов движка CatSystem2 авторства ShereKhanRomeo\n
ОГРОМНОЕ спасибо Trigger-Segfault за объяснения и ссылки на инструменты
Подробности на его вики: https://github.com/trigger-segfault/TriggersTools.CatSystem2/wiki \n\n
Ниже указаны файлы, которые ОБЯЗАТЕЛЬНО нужно скопировать в папку распаковщика из вашей папки с игрой:\n
0) cs2.exe       = главный файл игры, весит обычно 4-5 MB (скопируйте сюда и переименуйте в 'cs2')
   или cs2.bin   = если .ехе файл вашей игры весит меньше 1MB - скопируйте .bin файл вместо .ехе
                   (вес файла всё ещё должен быть 4-5 MB)\n
опциональные файлы, зависит от того, что вам нужно:
1) scene.int    = архив со скриптами сцен и текстом игры 
                  (не забудьте настроить также 'nametable.csv' при переводе - подробности на вики)
                  ('nametable.csv' обычно находится в 'config.ini')
2) image.int    = архив содержит изображения, ЦГшки из игры
3) movie.int    = архив содержит видео из игры
4) update00.int\n5) update01.int и все последующие 'updateXX.int' архивы\n
Файлы из каждого 'updateXX.int' архива перезаписывают соответствующие файлы из других .int-архивов,
включая файлы из 'updateXX.int' архивов с меньшим номером, так что лучше копируйте сюда все update-архивы.
После копирования всех архивов, подлежащих распаковке - нажмите Enter...\n""",
             "Копирование файлов в папку 'extracted' и распаковка 'int'-архивов может занимать до минуты на файл...",
             "Копирование {0}...",
             "Распаковка {0}...",
             "Удаление временных файлов...",
             "Сортировка получившихся файлов...",
             "Готово! Программа будет закрыта.",
             "Отсутствуют файлы в папке tools: {0}\nСкачайте или извлеките архив заново."]

locale_default = ["""Resources unpacker for CatSystem2 games by ShereKhanRomeo\n
HUGE thanks to Trigger-Segfault for explaining and tool links
check his wiki here https://github.com/trigger-segfault/TriggersTools.CatSystem2/wiki \n\n
Following game files are MANDATORY to be copied into folder with this unpacker:\n
0) cs2.exe      = main file of your game, it's usually 4 to 5 MB (copy here and rename into 'cs2')
   or cs2.bin   = if your game's .exe is less than 1MB - copy .bin file instead (it still should be 4 to 5 MB)\n
optional files, depends on what your goal is
1) scene.int    = file that contains game's scenes' script and text
                  (make sure to also adjust 'nametable.csv' while translating- see wiki)
                  ('nametable.csv' often can be found in 'config.ini')
2) image.int    = file that contains images
3) movie.int    = file that contains movies and videos
4) update00.int\n5) update01.int and all other 'updateXX.int' files\n
Files in each 'updateXX.int' archive overwrite according files from other int-archives,
including files from 'updateXX.int' archives with lesser number, so you better copy here all update-files.
After copying all files in this folder press Enter...""",
                  "Copying files into 'extracted' folder and unpacking 'int'-archives may take up to 1 minute per file...",
                  "Copying {0}...",
                  "Unpacking {0}...",
                  "Removing temporary files...",
                  "Sorting resulting files...",
                  "Done! Program will be closed now.",
                  "Following tools are missing: {0}\nDownload or unpack archive again."]

# other variables
dir_path = os.path.dirname(os.path.realpath(__file__)).replace("tools", "")
dir_path_extracted = dir_path + "extracted\\"
dir_path_tools = dir_path + "tools\\"
dir_path_extracted_animations = dir_path + "extracted\\animations\\"
dir_path_extracted_images = dir_path + "extracted\\images\\"
dir_path_extracted_movies = dir_path + "extracted\\movies\\"
dir_path_extracted_scripts = dir_path + "extracted\\scripts\\"
dir_path_extracted_sounds = dir_path + "extracted\\sounds\\"
dir_path_extracted_texts = dir_path + "extracted\\texts\\"
dir_path_extracted_clean_texts_for_translations = dir_path + "extracted\\clean texts for translations\\"

empty_character_name = "leave_empty"

exkifint_v3_exe = "exkifint_v3.exe"
game_main = "cs2.exe"
cs2_decompile_exe = "cs2_decompile.exe"
zlib1_dll = "zlib1.dll"
hgx2bmp_exe = "hgx2bmp.exe"
exzt_exe = "exzt.exe"

# i am ignoring kx2.ini archive for now, since i have no idea about .kx2-files it has inside
temp_archives = ["scene.int", "bgm.int", "config.int", "export.int", "fes.int", "image.int", "kcs.int", "mot.int",
                 "se.int", "ptcl.int", "movie.int", "update00.int", "update01.int", "update02.int", "update03.int", "update04.int"]
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
    create_if_not_exists(dir_path_extracted_animations)
    create_if_not_exists(dir_path_extracted_images)
    create_if_not_exists(dir_path_extracted_movies)
    create_if_not_exists(dir_path_extracted_scripts)
    create_if_not_exists(dir_path_extracted_sounds)
    create_if_not_exists(dir_path_extracted_texts)
    create_if_not_exists(dir_path_extracted_clean_texts_for_translations)


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
        print(str.format(locale_to_use[5], missing_files))
        press_any_key()
        sys.exit(0)


def copy_files_into_extract_folder():
    global game_main
    print(locale_to_use[1])
    dir_path_cs2_bin = dir_path + "\\cs2.bin"
    # TODO make unpacker check for correct file with VCODEs not to make user rename files
    if os.path.exists(dir_path_cs2_bin):
        os.chmod(dir_path_cs2_bin, 0o777)
        os.rename(dir_path_cs2_bin, dir_path + "\\cs2.exe")

    for file in temp_files:
        if os.path.exists(dir_path + "\\" + file):
            print(str.format(locale_to_use[2], file))
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
                print(str.format(locale_to_use[3], archive))
                call([exkifint_v3_exe, archive, game_main], stdin=None, stdout=None, stderr=None, shell=False)
        for archive in optional_voice_packages:
            archive_ini = dir_path_extracted + archive
            if os.path.exists(archive_ini):
                print(str.format(locale_to_use[3], archive))
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
                    print(str.format(locale_to_use[3], archive))
                    call([exzt_exe, archive], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted, ".zt")
    delete_file(dir_path_extracted + exzt_exe)
    delete_file(dir_path_extracted + zlib1_dll)
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
                print(str.format(locale_to_use[3], filename))
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
                print(str.format(locale_to_use[3], filename))
                call([cs2_decompile_exe, filename], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted_texts, ".cst")
    delete_file(dir_path_extracted_texts + cs2_decompile_exe)

    # extracting text lines from .txt files into .xlsx files
    extract_clean_text()
    os.chdir(dir_path)


def extract_clean_text():
    for filename in os.listdir(dir_path_extracted_texts):
        if os.path.isfile(filename) and filename.endswith(".txt"):
            print(str.format(locale_to_use[3], filename))
            encodingShiftJIS = "ShiftJIS"
            file_lines = []
            text_lines = []
            with codecs.open(dir_path_extracted_texts + filename, mode="rb", encoding=encodingShiftJIS) as file:
                file_lines = file.readlines()
                file.close()
            for line in file_lines[1:]:
                if line.endswith(TEXT_LINE_END1) or line.endswith(TEXT_LINE_END2) or line.startswith(SCENE_LINESTART1) or line.startswith(SCENE_LINESTART2):
                    # text lines we need for translation
                    text_lines.append(line)
                else:
                    # selection also contains links to parts according to player choice
                    # but also contain texts (!not always, be careful!) that we might wanna translate
                    selection = "fselect"
                    if selection in line:
                        next_index1 = file_lines.index(line) + 1
                        next_index2 = file_lines.index(line) + 2
                        next_index3 = file_lines.index(line) + 3
                        if len(file_lines) > next_index1:
                            if len(file_lines[next_index1].split(" ")) == 3:
                                # process linking
                                next_part = file_lines[next_index1].split(" ")[1]
                                # and add to list for translation
                                text_lines.append(file_lines[next_index1])
                        if len(file_lines) > next_index2:
                            if len(file_lines[next_index2].split(" ")) == 3:
                                # process linking
                                next_part = file_lines[next_index2].split(" ")[1]
                                # and add to list for translation
                                text_lines.append(file_lines[next_index2])
                        if len(file_lines) > next_index3:
                            if len(file_lines[next_index3].split(" ")) == 3:
                                # process linking
                                next_part = file_lines[next_index3].split(" ")[1]
                                # and add to list for translation
                                text_lines.append(file_lines[next_index3])

            column1_ids = []
            column2_names = []
            column3_lines = []
            for i in range(len(text_lines)):
                current_line = text_lines[i]
                if current_line.endswith(TEXT_LINE_END1) or current_line.endswith(TEXT_LINE_END2):
                    # if it's usual text line
                    text_line_parts = text_lines[i].split("\t")
                    if len(text_line_parts) == 2:
                        character_name = text_line_parts[0]
                        if len(character_name) == 0:
                            character_name = empty_character_name
                        column2_names.append(character_name)
                        column2_names.append(character_name)

                        text_line = text_line_parts[1]
                        # we need to remove "@" if present, but only if it's at the end of the line, not to remove "@" from inside the main text
                        column3_lines.append(text_line.replace(TEXT_LINE_END2, "").replace("\r\n", "").replace("\\fn", "").replace("[", "").replace("]", ""))
                        column3_lines.append(WRITE_TRANSLATION_HERE)
                        column1_ids.append(str.format(ORIGINAL_LINE_PATTERN, i))
                        column1_ids.append(str.format(TRANSLATION_LINE_PATTERN, i))
                    else:
                        # print("DEBUG " + str(len(text_line_parts)))
                        raise Exception("\n\n!!ERROR!!\nThere are lines with more that one TAB symbol in 1 line!\nThis is unexpected... "
                                        + "Please, contact developer on github with screenshot of this line:\n "
                                        + str(current_line.encode(encoding=encodingShiftJIS)) + "\n")

                elif current_line.startswith(SCENE_LINESTART1) or current_line.startswith(SCENE_LINESTART2):
                    # if it's scene title (naming)
                    column2_names.append(SCENE_TITLE)
                    column2_names.append(SCENE_TITLE)
                    column3_lines.append(current_line.replace(SCENE_LINESTART1, "").replace(SCENE_LINESTART2, "").replace("\r\n", ""))
                    column3_lines.append(WRITE_TRANSLATION_HERE)
                    column1_ids.append(str.format(ORIGINAL_LINE_PATTERN, i))
                    column1_ids.append(str.format(TRANSLATION_LINE_PATTERN, i))
                elif current_line.startswith("\t0") or current_line.startswith("\t1"):
                    # if it's choice line
                    column2_names.append(CHOICE_OPTION)
                    column2_names.append(CHOICE_OPTION)
                    # print("DEBUG " + str(current_line.encode(encoding=encodingShiftJIS)))
                    column3_lines.append(current_line.split(" ")[2].replace("\r\n", ""))
                    column3_lines.append(WRITE_TRANSLATION_HERE)
                    column1_ids.append(str.format(ORIGINAL_LINE_PATTERN, i))
                    column1_ids.append(str.format(TRANSLATION_LINE_PATTERN, i))
                    # print("DEBUG " + str(current_line.split(" ")[2].replace("　", " ").replace("_", " ").replace("|", " ").replace("\r\n", "").encode(encoding=encodingShiftJIS)))
                    # press_any_key()

            if len(column1_ids) > 0 and len(column2_names) > 0 and len(column3_lines) > 0:
                DataFrame({"Lines numbers": column1_ids, "Character name": column2_names, "Line text (!make sure to understand how nametable works before translating names!)": column3_lines}) \
                    .to_excel(dir_path_extracted_clean_texts_for_translations + filename.replace(".txt", ".xlsx"), sheet_name='sheet1', index=False)


def sort_resulting_files():
    print(locale_to_use[5])
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
            if file.endswith(".fes") or file.endswith(".kcs"):
                shutil.move(file, dir_path_extracted_scripts + filename)
            if file.endswith(".ogg") or file.endswith(".wav"):
                shutil.move(file, dir_path_extracted_sounds + filename)
            if file.endswith(".cst"):
                shutil.move(file, dir_path_extracted_texts + filename)

    os.chdir(dir_path)


def remove_temp_files():
    print(locale_to_use[4])
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
    for pth in os.listdir(dir_path_extracted):
        if os.path.isdir(dir_path_extracted + pth):
            with os.scandir(dir_path_extracted + pth) as it:
                if not any(it):
                    os.rmdir(dir_path_extracted + pth)


def clean_files_from_dir(_dir: str, _filetype: str):
    for filename in os.listdir(_dir):
        file = _dir + filename
        if file.endswith(_filetype):
            delete_file(file)


# core logic
if __name__ == '__main__':
    try:
        select_locale()
        check_all_tools_intact()
        print(locale_to_use[0])
        press_any_key()
        prepare_for_work()
        copy_files_into_extract_folder()
        extract_int_archives()
        extract_zt_archives()
        sort_resulting_files()

        unpack_images()

        unpack_texts()

        # contact me if you know tool for it
        # unpack_fes_scripts()

        # contact me if you know tool for it
        # unpack_kcs_scripts()

        # contact me if you know tool for it
        # unpack_animations()

    except Exception as error:
        print("ERROR - " + str("".join(traceback.format_exception(type(error),
                                                                  value=error,
                                                                  tb=error.__traceback__))).split(
            "The above exception was the direct cause of the following")[0])
    finally:
        remove_temp_files()
        remove_empty_folders()
        print(locale_to_use[6])  # done
