# CatSystem2 files unpacker

# locales to help more enthusiasts understand this tool
# just create new list with your translation and insert it into "select_locale()"
import ctypes
import locale
import os
import shutil
import sys
from subprocess import call

# locale[0] = intro
# locale[1] = removing temp files
# locale[2] = done! Enter to exit
# locale[3] = error missing files, Enter to exit

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
После копирования всех архивов, подлежащих распаковке - нажмите Enter...""",
             "Удаление временных файлов...",
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
                  "Removing temporary files...",
                  "Done! Program will be closed now.",
                  "Following tools are missing: {0}\nDownload or unpack archive again."]

# other variables
dir_path = os.path.dirname(os.path.realpath(__file__))
temp_files = ["cs2.exe", "scene.int", "image.int", "movie.int", "update00.int", "update01.int", "update02.int", "update03.int", "update04.int"]
temp_archives = ["scene.int", "image.int", "movie.int", "update00.int", "update01.int", "update02.int", "update03.int", "update04.int"]
temp_tools = ["convert.php", "Decat2.exe", "exkifint_v3.exe"]  ###, "extract_text_to_xlsx.py"]


# functions
def press_any_key():
    skip = input()


def create_if_not_exists(path_to_file_or_dir: str):
    global dir_path
    if not os.path.exists(dir_path + path_to_file_or_dir):
        os.mkdir(dir_path + path_to_file_or_dir)


def select_locale():
    global locale_ru, locale_default, locale_to_use
    match locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]:
        case 'ru_RU':
            locale_to_use = locale_ru
            return
        case _:
            locale_to_use = locale_default
            return


def create_folders():
    create_if_not_exists("/extracted")
    create_if_not_exists("/text")


def check_all_tools_intact():
    global dir_path, locale_to_use, temp_tools
    directory = dir_path + "/tools/"
    missing_files = ""
    for tool in temp_tools:
        if not os.path.exists(directory + tool):
            missing_files += tool + " "
    if len(missing_files) > 0:
        print(str.format(locale_to_use[3], missing_files))
        press_any_key()
        sys.exit(0)


def copy_files_into_exctract_folder():
    global temp_tools, temp_files
    if os.path.exists(dir_path + "/cs2.bin"):
        print("DEBUG - found cs2.bin, renaming into cs2.exe...")
        os.rename(dir_path + "/cs2.bin", dir_path + "/cs2.exe")

    for file in temp_files:
        if os.path.exists(dir_path + "/" + file):
            print("DEBUG - copying " + file + " into 'extracted'...")
            os.chmod(dir_path + "/" + file, 0o777)
            shutil.copy(dir_path + "/" + file, dir_path + "/extracted/" + file)
    for file in temp_tools:
        if os.path.exists(dir_path + "/tools/" + file):
            print("DEBUG - copying " + file + " into 'extracted'...")
            os.chmod(dir_path + "/tools/" + file, 0o777)
            shutil.copy(dir_path + "/tools/" + file, dir_path + "/extracted/" + file)


def remove_temp_files():
    global temp_tools, temp_files
    for file in temp_files:
        if os.path.exists(dir_path + "/extracted/" + file):
            print("DEBUG - removing temp file " + file + "...")
            os.remove(dir_path + "/extracted/" + file)
    for file in temp_tools:
        if os.path.exists(dir_path + "/extracted/" + file):
            print("DEBUG - removing temp file " + file + "...")
            os.remove(dir_path + "/extracted/" + file)
    for filename in os.listdir(dir_path + "/extracted/"):
        file = dir_path + "/extracted/" + filename
        if file.endswith(".out"):
            print("DEBUG - removing temp file " + filename + "...")
            os.remove(file)


def extract_everything():
    global temp_archives
    # first unpacking from int archives
    exkifint_v3_exe = dir_path + "/extracted/exkifint_v3.exe"
    cs2_exe = dir_path + "/extracted/cs2.exe"
    decat2_exe = dir_path + "/extracted/Decat2.exe"
    convert_php = dir_path + "/extracted/convert.php"
    if os.path.exists(exkifint_v3_exe) and os.path.exists(cs2_exe):
        for archive in temp_archives:
            archive_ini = dir_path + "/extracted/" + archive
            if os.path.exists(archive_ini):
                print("DEBUG - exkifinting file " + archive_ini + "...")
                # TODO завернуть в батник, чтобы вызов был в папке extracted
                call([exkifint_v3_exe, archive_ini, cs2_exe], stdin=None, stdout=None, stderr=None, shell=False)

    # next unpacking .cst files to .out files
    if os.path.exists(decat2_exe):
        for filename in os.listdir(dir_path + "/extracted/"):
            file = dir_path + "/extracted/" + filename
            if file.endswith(".cst"):
                print("DEBUG - decatting file " + file + "...")
                call([decat2_exe + " " + file], stdin=None, stdout=None, stderr=None, shell=False)

    # next unpacking .out files to .txt files
    if os.path.exists(convert_php):
        for filename in os.listdir(dir_path + "/extracted/"):
            file = dir_path + "/extracted/" + filename
            if file.endswith(".out"):
                print("DEBUG - converting file " + file + "...")
                call(["php " + convert_php + " " + file], stdin=None, stdout=None, stderr=None, shell=False)

    # TODO next extracting text lines from .txt files into .xlsx files
    pass


# core logic
if __name__ == '__main__':
    try:
        select_locale()
        create_folders()
        check_all_tools_intact()
        print(locale_to_use[0])
        press_any_key()

        copy_files_into_exctract_folder()
        extract_everything()
    except Exception as ex:
        print("ERROR - " + str(ex))
    finally:
        print(locale_to_use[1])
        remove_temp_files()
        print(locale_to_use[2])


