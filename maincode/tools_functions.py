
def split_ch(string:str, char:str)->list:
    word = ""
    l = []
    for letter in string:
        if letter == char or letter == "\n":
            l.append(word)
            word = ""
        else:
            word += letter
    return l