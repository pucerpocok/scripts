#! /bin/python3

import string

#TODO: remove hardcoding
# create the base64 table (see wikipedia:base64)
base64_table = {
        "000000": "A",
        "000001": "B",
        "000010": "C",
        "000011": "D",
        "000100": "E",
        "000101": "F",
        "000110": "G",
        "000111": "H",
        "001000": "I",
        "001001": "J",
        "001010": "K",
        "001011": "L",
        "001100": "M",
        "001101": "N",
        "001110": "O",
        "001111": "P",
        "010000": "Q",
        "010001": "R",
        "010010": "S",
        "010011": "T",
        "010100": "U",
        "010101": "V",
        "010110": "W",
        "010111": "X",
        "011000": "Y",
        "011001": "Z",
        "011010": "a",
        "011011": "b",
        "011100": "c",
        "011101": "d",
        "011110": "e",
        "011111": "f",
        "100000": "g",
        "100001": "h",
        "100010": "i",
        "100011": "j",
        "100100": "k",
        "100101": "l",
        "100110": "m",
        "100111": "n",
        "101000": "o",
        "101001": "p",
        "101010": "q",
        "101011": "r",
        "101100": "s",
        "101101": "t",
        "101110": "u",
        "101111": "v",
        "110000": "w",
        "110001": "x",
        "110010": "y",
        "110011": "z",
        "110100": "0",
        "110101": "1",
        "110110": "2",
        "110111": "3",
        "111000": "4",
        "111001": "5",
        "111010": "6",
        "111011": "7",
        "111100": "8",
        "111101": "9",
        "111110": "+",
        "111111": "/",
}

rev_base64_table = {v: k for k, v in base64_table.items()}

en_alphabet = {
    "e": 12.702,
    "t": 9.056,
    "a": 8.167,
    "o": 7.507,
    "i": 6.966,
    "n": 6.749,
    "s": 6.327,
    "h": 6.094,
    "r": 5.987,
    "d": 4.253,
    "l": 4.025,
    "c": 2.782,
    "u": 2.758,
    "m": 2.406,
    "w": 2.360,
    "f": 2.228,
    "g": 2.015,
    "y": 1.974,
    "p": 1.929,
    "b": 1.492,
    "v": 0.978,
    "k": 0.772,
    "j": 0.153,
    "x": 0.150,
    "q": 0.095,
    "z": 0.074,
}


def hex_decode(s):
    s0 = ''
    for c in range(0, len(s), 2):
        s0 += chr(int(s[c:c+2], 16))
    return s0

def hex_encode(s):
    s0 = ''
    for c in s:
        s0 += '{}'.format(hex(ord(c))[2:]).rjust(2, '0')
    return s0

def str_to_bin(s):
    return ''.join(format(ord(x), 'b').rjust(8, '0') for x in s)

def bin_to_str(s):
    s = ''.join(s.split(' '))
    return ''.join(chr(int(s[i:i+8], 2)) for i in range(0, len(s)) if i%8==0)

def bin_to_base64(s):
    # TODO: UGLY
    s0 = ''
    x = None
    for i in range(len(s)):
        if i % 6 == 0:
            try:
                s0 += base64_table[s[i:i+6]]
            except KeyError:
                x = i
    if x is not None:
        if (len(s[x:x+6]) + 8) % 6 == 0:
            s0 += base64_table[s[x:x+6]+"00"]
            s0 += "="
        else:
            s0 += base64_table[s[x:x+6]+"0000"]
            s0 += "=="
    return s0

def base64_to_bin(s):
    # TODO: padding at the end will be interpreted as 'A'
    s0 = ''
    for c in s:
        try:
            s0 += rev_base64_table[c]
        except KeyError:
            s0 += "000000"
    if s0[-8:] == "00000000":
        s0 = s0[:-8]
    return s0

def hex_string_to_base64(s):
    s0 = hex_decode(s)
    s1 = str_to_bin(s0)
    s2 = bin_to_base64(s1)
    return s2

def fixed_xor(s1, s2):
    s3 = ''
    for i in range(len(s1)):
        s3 += '0' if s1[i] == s2[i] else '1'
    return s3

def single_byte_xor(s, c):
    s0 = ''
    for i in range(len(s)):
        if i % 8 == 0:
            s0 += fixed_xor(s[i:i+8], c)
    return s0

def repeating_xor(plain, key):
    i = 0
    s = ""
    for c in plain:
        s += bin_to_str(fixed_xor(str_to_bin(c), str_to_bin(key[i])))
        i += 1
        if i == len(key):
            i = 0
    return s#hex_encode(s)


#TODO: additional scoring methods are needed
def scoring(s):
    score = 0
    contains_non_printable = False
    number_of_spaces = 0
    vowels = 0
    frequency_table = {}
    frequency_table["other"] = 0
    for c in s:
        c = c.lower()
        if c not in string.printable:
            # if it contains non-printable character,
            # most probably it is not a human readable text
            contains_non_printable = True
        if c not in en_alphabet.keys():
            frequency_table["other"] += 1
            if c == " ":
                number_of_spaces += 1
        else:
            if c not in frequency_table.keys():
                frequency_table[c] = 1
            else:
                frequency_table[c] += 1
            if c in "euioa":
                vowels += 1
    if not contains_non_printable:
        score += 20
    if number_of_spaces > 0:
        diff = number_of_spaces / len(s)
        if 0.1 <= diff and diff <= 0.3:
            score += 20
    if vowels > 0:
        diff = vowels / len(s)
        if 0.2 <= diff and diff <= 0.5:
            score += 10
    return score

def hamming_distance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))
