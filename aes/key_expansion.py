# AES Key Expansion

import re
import math
import hashlib, base64

def text_to_matrix(text):
    matrix = []
    for i in range(16):
        byte = (text >> (8 * (15 - i))) & 0xFF                      # pegando 1 byte do texto 
        if i % 4 == 0:
            matrix.append([byte])                                   # criando uma linha nova no 'block cipher' pros bytes de texto que foram claculados
        else:
            matrix[i // 4].append(byte)                             # adicionando o 'block cipher' de bytes na matriz de 16 elementos que eh usada no metodo AES
    return matrix  

def rot_word(key: str):
    """Rotates the word by one byte to the left"""
    return key[2:] + key[:2]

