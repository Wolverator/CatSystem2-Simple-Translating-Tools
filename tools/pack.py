import ctypes
import locale
import os
import shutil
import sys
import traceback

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


temp_tools = [hgx2bmp_exe, zlib1_dll, exzt_exe, exkifint_v3_exe, cs2_decompile_exe]


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
locale_to_use = []
# TODO finish descriptions
locale_ru = ["""Упаковщик ресурсов движка CatSystem2 авторства ShereKhanRomeo\n
ОГРОМНОЕ спасибо Trigger-Segfault за объяснения и ссылки на инструменты
Подробности на его вики: https://github.com/trigger-segfault/TriggersTools.CatSystem2/wiki \n\n
В архив {0} будут упакованы все файлы из папки "extracted" - нажмите Enter, чтобы начать...\n""",
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
All files from "extracted" folder will be compiled into {0} archive -  press Enter to start...""",
                  "Copying files into 'extracted' folder and unpacking 'int'-archives may take up to 1 minute per file...",
                  "Copying {0}...",
                  "Unpacking {0}...",
                  "Removing temporary files...",
                  "Sorting resulting files...",
                  "Done! Program will be closed now.",
                  "Following tools are missing: {0}\nDownload or unpack archive again."]



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
        # pack_images()

        pack_texts()


    except Exception as error:
        print("ERROR - " + str("".join(traceback.format_exception(type(error),
                                                                  value=error,
                                                                  tb=error.__traceback__))).split(
            "The above exception was the direct cause of the following")[0])
    finally:
        #remove_temp_files()
        remove_empty_folders()
        print(locale_to_use[6])  # done
