import os
path = os.path.dirname(os.path.realpath(__file__)) + "\\result_sherhan\\texts"
#path = os.path.dirname(os.path.realpath(__file__)) + "\\extracted_steam\\texts"
#path = os.path.dirname(os.path.realpath(__file__)) + "\\extracted_18\\texts"
in_files = ".txt"
encod = "ShiftJIS"

phrase_we_look_for = "\\fn\n" #case sensitive!

lulz = ['0','1','2','3','4','5','6','7','8','9','!','#','@','[',']','\\','?','&','"','-','+','=',',','.','(',')','\t','\n', 
    '\r','`',':',';','-','_',' ','*','%','$','^','<','>','―','”','“','\`','　','/',"'",'〜','♪','─','’','~','●','|','0','0','0',
    '0','0','0','0','0','0','0','0','0','0','0','0',
    'Z','Y','X','W','V','U','T','S','R','Q','P','O','N','M','L','K','J','I','H','G','F','E','D','C','B','A',
    'z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']


def scan(path1):
    for f1 in os.listdir(path1):
        if os.path.isdir(os.path.join(path1, f1)):
            scan(os.path.join(path1, f1))
        if os.path.isfile(os.path.join(path1, f1)) and os.path.join(path1, f1).endswith(in_files):
            with open(os.path.join(path1, f1), mode='r', encoding=encod) as ff1:
                found = False
                text_lines = ff1.readlines()
                for i in range(len(text_lines)):
                    for j in range(len(text_lines[i])):
                        if text_lines[i][j] not in lulz:
                            found = True
                            print("================================================================")
                            #print(text_lines[i-2].replace("\n", "").replace("[", "").replace("]", ""))
                            #print(text_lines[i-1].replace("\n", "").replace("[", "").replace("]", ""))
                            print(text_lines[i].replace("\n", "").replace("[", "").replace("]", ""))
                            #print((text_lines[i+1].replace("\n", "").replace("[", "").replace("]", "")))
                            #print(text_lines[i+2].replace("\n", "").replace("[", "").replace("]", ""))
                if found:
                    print("◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘ FOUND IN " + os.path.join(path1, f1) + " ◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘")

print("SEARCH START...")
scan(path)
print("FINISHED")


                # text = ff1.read()
                # if phrase_we_look_for in text:
                    # found = True
                    # teset = text.partition(phrase_we_look_for)[2][:9]
                    # print([ch for ch in teset])
                    
                    
                    
                    
                    
                    # text_lines = ff1.readlines()
                # for i in range(len(text_lines)):
                    # if phrase_we_look_for in text_lines[i]\
                        # and text_lines[i+1].replace("\n", "").replace("\t", "") is not ""\
                        # and text_lines[i+1].replace("\n", "") is not "":
                        # found = True
                        # print("================================================================")
                        # #print(text_lines[i-2].replace("\n", "").replace("[", "").replace("]", ""))
                        # #print(text_lines[i-1].replace("\n", "").replace("[", "").replace("]", ""))
                        # print(text_lines[i].replace("\n", "").replace("[", "").replace("]", ""))
                        # print((text_lines[i+1].replace("\n", "").replace("[", "").replace("]", "")))
                        # #print(text_lines[i+2].replace("\n", "").replace("[", "").replace("]", ""))
                # if found:
                    # print("◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘ FOUND IN " + os.path.join(path1, f1) + " ◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘")