import os

path = os.path.dirname(os.path.realpath(__file__)) + "\\old_extracted\\texts\\"
in_files = ".txt" # в файлах какого формата ищем
file_encoding = "ShiftJIS" #какую кодировку файлов ожидаем (у РенПая обычно UTF-8)

phrase_we_look_for = "Makina+Yumiko" #case sensitive! (usually) // Чувствительно к регистру (обычно)


def scan(path1):
    for f1 in os.listdir(path1):
        if os.path.isdir(os.path.join(path1, f1)):
            scan(os.path.join(path1, f1))
        if os.path.isfile(os.path.join(path1, f1)) and os.path.join(path1, f1).endswith(in_files):
            with open(os.path.join(path1, f1), mode='r', encoding=file_encoding) as ff1:
                found = False
                print("searching in " + os.path.join(path1, f1) + "...")
                for line in ff1.readlines():
                    if phrase_we_look_for in line:
                        found = True
                        print(line.replace("\r", "").replace("\n", "").replace("\fn", "").replace("[", "").replace("]", ""))
                if found:
                    print("======== FOUND IN " + os.path.join(path1, f1) + " ========\n")

print("SEARCH START...")
scan(path)
print("FINISHED")