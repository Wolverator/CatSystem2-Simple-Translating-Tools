import os

path = os.path.dirname(os.path.realpath(__file__)) #+ "\\extracted\\texts"
in_files = ".txt"
encod = "ShiftJIS"
#print("path= " + path)

phrase_we_look_for = "@" #case sensitive!


def scan(path1):
    for f1 in os.listdir(path1):
        if os.path.isfile(os.path.join(path1, f1)) and os.path.join(path1, f1).endswith(in_files):
            with open(os.path.join(path1, f1), mode='r', encoding=encod) as ff1:
                for line in ff1.readlines():
                    found = False
                    if line.endswith("\\fn\r\n") or line.endswith("@\r\n") and phrase_we_look_for in line.replace("@\r\n", ""):
                        found = True
                        print(line)
                    if found:
                        print("FOUND IN " + os.path.join(path1, f1) + "\n")

scan(path)
print("FINISHED")