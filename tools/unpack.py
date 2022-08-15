import ctypes
import locale
import os
import shutil
import sys
import traceback
from subprocess import call

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
             "\nКопирование файлов в папку 'extracted', может занимать до минуты на файл...",
             "\nКопирование {0}...",
             "\nРаспаковка {0}...",
             "\nУдаление временных файлов...",
             "\nСортировка получившихся файлов...",
             "\nГотово! Программа будет закрыта.",
             "\nОтсутствуют файлы в папке tools: {0}\nСкачайте или извлеките архив заново."]

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
                  "\nCopying files into 'extracted' folder, may take up to 1 minute per file...",
                  "\nCopying {0}...",
                  "\nUnpacking {0}...",
                  "\nRemoving temporary files...",
                  "\nSorting resulting files...",
                  "\nDone! Program will be closed now.",
                  "\nFollowing tools are missing: {0}\nDownload or unpack archive again."]

# other variables
dir_path = os.path.dirname(os.path.realpath(__file__)).replace("tools", "")
print(dir_path)
dir_path_extracted = dir_path + "extracted\\"
dir_path_tools = dir_path + "tools\\"
dir_path_extracted_animations = dir_path + "extracted\\animations\\"
dir_path_extracted_images = dir_path + "extracted\\images\\"
dir_path_extracted_movies = dir_path + "extracted\\movies\\"
dir_path_extracted_scripts = dir_path + "extracted\\scripts\\"
dir_path_extracted_sounds = dir_path + "extracted\\sounds\\"
dir_path_extracted_texts = dir_path + "extracted\\texts\\"

exkifint_v3_exe = "exkifint_v3.exe"
cs2_exe = "cs2.exe"
decat2_exe = "Decat2.exe"
convert_php = "convert.php"
zlib1_dll = "zlib1.dll"
hgx2bmp_exe = "hgx2bmp.exe"
exzt_exe = "exzt.exe"

# i am ignoring kx2.ini archive for now, since i have no idea about .kx2-files it has inside
temp_archives = ["scene.int", "bgm.int", "config.int", "export.int", "fes.int", "image.int", "kcs.int", "mot.int",
                 "se.int", "ptcl.int", "movie.int", "update00.int", "update01.int", "update02.int", "update03.int", "update04.int"]
temp_files = temp_archives.copy()
temp_files.append(cs2_exe)
temp_tools = [convert_php, decat2_exe, hgx2bmp_exe, zlib1_dll, exzt_exe, exkifint_v3_exe]  ###, "extract_text_to_xlsx.py"]
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
    print(locale_to_use[1])
    dir_path_cs2_bin = dir_path + "\\cs2.bin"
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
            and os.path.exists(dir_path_extracted + cs2_exe):
        for archive in temp_archives:
            archive_ini = dir_path_extracted + archive
            if os.path.exists(archive_ini):
                print(str.format(locale_to_use[3], archive))
                call([exkifint_v3_exe, archive, cs2_exe], stdin=None, stdout=None, stderr=None, shell=False)
        for archive in optional_voice_packages:
            archive_ini = dir_path_extracted + archive
            if os.path.exists(archive_ini):
                print(str.format(locale_to_use[3], archive))
                call([exkifint_v3_exe, archive, cs2_exe], stdin=None, stdout=None, stderr=None, shell=False)
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
    # os.chmod(dir_path_extracted_images + hgx2bmp_exe, 0o777)
    # os.chmod(dir_path_extracted_images + zlib1_dll, 0o777)
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
    shutil.copy(dir_path_tools + decat2_exe, dir_path_extracted_texts + decat2_exe)
    if os.path.exists(dir_path_extracted_texts + decat2_exe):
        for filename in os.listdir(dir_path_extracted_texts):
            file = dir_path_extracted_texts + filename
            if file.endswith(".cst"):
                print(str.format(locale_to_use[3], filename))
                call([decat2_exe, filename], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted_texts, ".cst")
    delete_file(dir_path_extracted_texts + decat2_exe)

    # next unpacking .out files to .txt files
    shutil.copy(dir_path_tools + convert_php, dir_path_extracted_texts + convert_php)
    if os.path.exists(convert_php):
        for filename in os.listdir(dir_path_extracted_texts):
            file = dir_path_extracted_texts + filename
            if file.endswith(".out"):
                print(str.format(locale_to_use[3], filename))
                call(["php", convert_php, file], stdin=None, stdout=None, stderr=None, shell=False)
    clean_files_from_dir(dir_path_extracted_texts, ".out")
    delete_file(dir_path_extracted_texts + convert_php)
    # TODO next extracting text lines from .txt files into .xlsx files
    os.chdir(dir_path)


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
