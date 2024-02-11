import os
import pandas
from colorama import Fore, init

init(autoreset=True)
path = os.path.dirname(os.path.realpath(__file__))
in_files = ".xlsx" # files of what format are being searched
file_encoding = "ShiftJIS" #  (RenPy usually uses UTF-8)

phrase_we_look_for = "Казами-сан" #case sensitive! (usually)


def scan(path1):
    for f1 in os.listdir(path1):
        filepath = os.path.join(path1, f1)
        if os.path.isdir(filepath):
            scan(filepath)
        if os.path.isfile(filepath) and filepath.endswith(in_files) and not f1.startswith("~"):
            xlsx_file = pandas.ExcelFile(filepath)
            df = xlsx_file.parse(xlsx_file.sheet_names[0])
            found = False
            if 'Line text' in df.keys():
                for line in df['Line text']:
                    try:
                        if phrase_we_look_for in str(line).replace("[", "").replace("]", ""):
                            found = True
                            print(line.replace("\r", "").replace("\n", "").replace("\fn", "").replace("[", "").replace("]", ""))
                    except Exception as error:
                        print(line)
                        print(filepath)
                        raise error
                if found:
                        print(Fore.GREEN + "======== FOUND IN " + filepath + " ========\n")

if __name__ == "__main__":
    print("SEARCH START...")
    scan(path)
    print("FINISHED")
    print("You can close the program manually or press any key to do so.")
    skip = input()
