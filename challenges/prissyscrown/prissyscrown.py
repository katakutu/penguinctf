import md5

def pythonpit():
    crown = [
        36, 46, 35, 37, 57,
        27, 45, 55, 29, 3,
        44, 38, 29, 15, 39,
        29, 0, 35, 32, 59,
        29, 3, 43, 44, 54,
        29, 12, 45, 54, 42,
        43, 44, 37, 29, 0,
        55, 54, 29, 15, 35,
        47, 47, 35, 46, 49,
        63
    ]
    magic_key = int(raw_input("The Royal Crown Only Responds to a Penguin of Purity: "))
    build_snowman(crown, magic_key)

def build_snowman(data, byte):
    flag = ""
    for i in data:
        flag += chr(i ^ byte)
    if md5.md5(flag).hexdigest() == "6aad017de0ab1afec5b996b7445a0bf9":
        print "You've got it! The flag is: %s" % flag
    else:
        print "You've failed to retrieve the crown. You are an embarassment."

# Flag is flag{You_And_Me_Baby_Aint_Nothing_But_Mammals}
