def bin_as_int(x):
    return int(x, 2)


# Generate a char/string representation of decimals
def dec_to_string(decimals):
    chars = []
    for i in decimals:
        chars.append(chr(i))

    # Generate a string representation
    string_representation = ""
    for c in chars:
        string_representation += c

    # print("string :", end=" ")
    # print(string_representation)
    return string_representation


# Generate a binary represantation (string of 0s and 1s) of decimals
def dec_to_bin(decimals):
    string = ""
    for x in decimals:
        # print(bin(x), end=" ")
        string += bin(x) + " "
    return string
