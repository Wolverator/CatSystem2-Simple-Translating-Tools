import os

path = "D:/Misc/VNs/Grisaia 1 debug/source game files/texts"
in_files = ".txt" # files of what format are being searched
file_encoding = "ShiftJIS" #  (RenPy usually uses UTF-8)

phrase_we_look_for = "%" #case sensitive! (usually)


def scan(path1):
    for f1 in os.listdir(path1):
        if os.path.isdir(os.path.join(path1, f1)):
            scan(os.path.join(path1, f1))
        if os.path.isfile(os.path.join(path1, f1)) and os.path.join(path1, f1).endswith(in_files):
            with open(os.path.join(path1, f1), mode='r', encoding=file_encoding) as ff1:
                found = False
                for line in ff1.readlines():
                    if phrase_we_look_for in line:
                        found = True
                        print(line.replace("\r", "").replace("\n", "").replace("\fn", "").replace("[", "").replace("]", ""))
                if found:
                    print("======== FOUND IN " + os.path.join(path1, f1) + " ========\n")

print("SEARCH START...")
scan(path)
print("FINISHED")
skip = input()
time.sleep(10)