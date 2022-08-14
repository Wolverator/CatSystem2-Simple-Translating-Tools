import os

path = os.path.dirname(os.path.realpath(__file__)) + "\\text"
in_files = ".txt"
encod = "UTF-8"
#print("path= " + path)

phrase_we_look_for = "Unrated" #case sensitive!


def scan(path):
    for f1 in os.listdir(path1):
        if os.path.isfile(os.path.join(path1, f1)):
            if os.path.join(path1, f1).endswith(in_files):
                with open(os.path.join(path1, f1), mode='r', encoding=encod) as ff1:
                    if phrase_we_look_for in ff1.read():
                        print("FOUND IN " + os.path.join(path1, f1))

scan(path)
print("FINISHED")