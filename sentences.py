

import random as rn
import string


def generate_chunk(lenght = 5, numbers = True, symbols = True, uppercase = True):
    chars = string.ascii_lowercase
    if numbers:
        chars +=string.digits
    if uppercase:
        chars += string.ascii_uppercase
    if symbols:
        chars += "~!@#$%^&*())-_"  
    return "".join(rn.choice(chars) for _ in range(lenght))

def generate_string(chunks=5,chunk_length=5 , **kwargs):
    return ' '.join(generate_chunk(chunk_length, **kwargs) for _ in range(chunks))

