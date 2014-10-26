flag = "flag{This_Is_A_Flag}"

def flag_check(flag, submit):
    def process(data):
        # All to lowercase
        ret = data.lower()
        if ret[:5] == "flag{":
            ret = ret[5:-1]
        return ret

    return process(flag) == process(submit)

inp = [
    "This_Is_A_Flag", "flag{This_Is_A_Flag}",
    "flag{this_is_a_flag}", "this_is_a_flag" 
    ,"flag{nikisacoward}"
    ]

for i in inp:
    print "%s: %s" % (i, str(flag_check(flag, i)))

