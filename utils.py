def bin_int(x):
    return int(x, 2)


def dec_to_string(decimals_list):
    # Generate a char/string representation of decimals
    char_list = []
    for num in decimals_list:
        char_list.append(chr(num))
    # Generate a string representation
    string_representation = ""
    for c in char_list:
        string_representation += c
    # print("string :", end=" ")
    # print(string_representation)
    return string_representation


def dec_to_bin(decimals_list):
    # Generate a binary represantation
    # print("binary :", end=" ")
    string = ""
    for x in decimals_list:
        # print(bin(x), end=" ")
        string += bin(x) + " "
    return string