import aes.utils as utils
import aes.key_expansion as expansion

REVERSED_SBOX = [
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
]

E_TABLE = [ 
    0x01, 0x03, 0x05, 0x0F, 0x11, 0x33, 0x55, 0xFF, 0x1A, 0x2E, 0x72, 0x96, 0xA1, 0xF8, 0x13, 0x35,
    0x5F, 0xE1, 0x38, 0x48, 0xD8, 0x73, 0x95, 0xA4, 0xF7, 0x02, 0x06, 0x0A, 0x1E, 0x22, 0x66, 0xAA,
    0xE5, 0x34, 0x5C, 0xE4, 0x37, 0x59, 0xEB, 0x26, 0x6A, 0xBE, 0xD9, 0x70, 0x90, 0xAB, 0xE6, 0x31,
    0x53, 0xF5, 0x04, 0x0C, 0x14, 0x3C, 0x44, 0xCC, 0x4F, 0xD1, 0x68, 0xB8, 0xD3, 0x6E, 0xB2, 0xCD,
    0x4C, 0xD4, 0x67, 0xA9, 0xE0, 0x3B, 0x4D, 0xD7, 0x62, 0xA6, 0xF1, 0x08, 0x18, 0x28, 0x78, 0x88,
    0x83, 0x9E, 0xB9, 0xD0, 0x6B, 0xBD, 0xDC, 0x7F, 0x81, 0x98, 0xB3, 0xCE, 0x49, 0xDB, 0x76, 0x9A,
    0xB5, 0xC4, 0x57, 0xF9, 0x10, 0x30, 0x50, 0xF0, 0x0B, 0x1D, 0x27, 0x69, 0xBB, 0xD6, 0x61, 0xA3,
    0xFE, 0x19, 0x2B, 0x7D, 0x87, 0x92, 0xAD, 0xEC, 0x2F, 0x71, 0x93, 0xAE, 0xE9, 0x20, 0x60, 0xA0,
    0xFB, 0x16, 0x3A, 0x4E, 0xD2, 0x6D, 0xB7, 0xC2, 0x5D, 0xE7, 0x32, 0x56, 0xFA, 0x15, 0x3F, 0x41,
    0xC3, 0x5E, 0xE2, 0x3D, 0x47, 0xC9, 0x40, 0xC0, 0x5B, 0xED, 0x2C, 0x74, 0x9C, 0xBF, 0xDA, 0x75,
    0x9F, 0xBA, 0xD5, 0x64, 0xAC, 0xEF, 0x2A, 0x7E, 0x82, 0x9D, 0xBC, 0xDF, 0x7A, 0x8E, 0x89, 0x80,
    0x9B, 0xB6, 0xC1, 0x58, 0xE8, 0x23, 0x65, 0xAF, 0xEA, 0x25, 0x6F, 0xB1, 0xC8, 0x43, 0xC5, 0x54,
    0xFC, 0x1F, 0x21, 0x63, 0xA5, 0xF4, 0x07, 0x09, 0x1B, 0x2D, 0x77, 0x99, 0xB0, 0xCB, 0x46, 0xCA,
    0x45, 0xCF, 0x4A, 0xDE, 0x79, 0x8B, 0x86, 0x91, 0xA8, 0xE3, 0x3E, 0x42, 0xC6, 0x51, 0xF3, 0x0E,
    0x12, 0x36, 0x5A, 0xEE, 0x29, 0x7B, 0x8D, 0x8C, 0x8F, 0x8A, 0x85, 0x94, 0xA7, 0xF2, 0x0D, 0x17,
    0x39, 0x4B, 0xDD, 0x7C, 0x84, 0x97, 0xA2, 0xFD, 0x1C, 0x24, 0x6C, 0xB4, 0xC7, 0x52, 0xF6, 0x01 
]

L_TABLE = [ 
    0x00, 0x00, 0x19, 0x01, 0x32, 0x02, 0x1A, 0xC6, 0x4B, 0xC7, 0x1B, 0x68, 0x33, 0xEE, 0xDF, 0x03,
    0x64, 0x04, 0xE0, 0x0E, 0x34, 0x8D, 0x81, 0xEF, 0x4C, 0x71, 0x08, 0xC8, 0xF8, 0x69, 0x1C, 0xC1,
    0x7D, 0xC2, 0x1D, 0xB5, 0xF9, 0xB9, 0x27, 0x6A, 0x4D, 0xE4, 0xA6, 0x72, 0x9A, 0xC9, 0x09, 0x78,
    0x65, 0x2F, 0x8A, 0x05, 0x21, 0x0F, 0xE1, 0x24, 0x12, 0xF0, 0x82, 0x45, 0x35, 0x93, 0xDA, 0x8E,
    0x96, 0x8F, 0xDB, 0xBD, 0x36, 0xD0, 0xCE, 0x94, 0x13, 0x5C, 0xD2, 0xF1, 0x40, 0x46, 0x83, 0x38,
    0x66, 0xDD, 0xFD, 0x30, 0xBF, 0x06, 0x8B, 0x62, 0xB3, 0x25, 0xE2, 0x98, 0x22, 0x88, 0x91, 0x10,
    0x7E, 0x6E, 0x48, 0xC3, 0xA3, 0xB6, 0x1E, 0x42, 0x3A, 0x6B, 0x28, 0x54, 0xFA, 0x85, 0x3D, 0xBA,
    0x2B, 0x79, 0x0A, 0x15, 0x9B, 0x9F, 0x5E, 0xCA, 0x4E, 0xD4, 0xAC, 0xE5, 0xF3, 0x73, 0xA7, 0x57,
    0xAF, 0x58, 0xA8, 0x50, 0xF4, 0xEA, 0xD6, 0x74, 0x4F, 0xAE, 0xE9, 0xD5, 0xE7, 0xE6, 0xAD, 0xE8,
    0x2C, 0xD7, 0x75, 0x7A, 0xEB, 0x16, 0x0B, 0xF5, 0x59, 0xCB, 0x5F, 0xB0, 0x9C, 0xA9, 0x51, 0xA0,
    0x7F, 0x0C, 0xF6, 0x6F, 0x17, 0xC4, 0x49, 0xEC, 0xD8, 0x43, 0x1F, 0x2D, 0xA4, 0x76, 0x7B, 0xB7,
    0xCC, 0xBB, 0x3E, 0x5A, 0xFB, 0x60, 0xB1, 0x86, 0x3B, 0x52, 0xA1, 0x6C, 0xAA, 0x55, 0x29, 0x9D,
    0x97, 0xB2, 0x87, 0x90, 0x61, 0xBE, 0xDC, 0xFC, 0xBC, 0x95, 0xCF, 0xCD, 0x37, 0x3F, 0x5B, 0xD1,
    0x53, 0x39, 0x84, 0x3C, 0x41, 0xA2, 0x6D, 0x47, 0x14, 0x2A, 0x9E, 0x5D, 0x56, 0xF2, 0xD3, 0xAB,
    0x44, 0x11, 0x92, 0xD9, 0x23, 0x20, 0x2E, 0x89, 0xB4, 0x7C, 0xB8, 0x26, 0x77, 0x99, 0xE3, 0xA5,
    0x67, 0x4A, 0xED, 0xDE, 0xC5, 0x31, 0xFE, 0x18, 0x0D, 0x63, 0x8C, 0x80, 0xC0, 0xF7, 0x70, 0x07 
]

#decifrador no modo ECB
def decripter_ECB(nomeArquivo, key, rounds):
    bytes_decripted = b''

    sub_keys = expansion.expand_key_int(16, key)

    blocks_4bytes = utils.dec_prepare_mensage_ecb(nomeArquivo)

    for i in range(0, len(blocks_4bytes), 4):
        aux = dec_aes(blocks_4bytes[i: i + 4], sub_keys, rounds)
        for j in range(4):
            bytes_decripted = bytes_decripted + aux[j].to_bytes(4, 'big')
    
    bytes_added = bytes_decripted[len(bytes_decripted) - 1]
    bytes_decripted = bytes_decripted[0:len(bytes_decripted) - bytes_added]

    with open('decifrado_ecb.txt', 'wb') as a:
        a.write(bytes_decripted)
        a.close
    
    return bytes_decripted

#bloco de decifrador AES. Recebe o bloco de 16bytes em forma de uma lista com 4 bytes cada elemento
#recebe as subchaves em uma lista com 4 bytes cada elemento e o numero de rodas
def dec_aes(block , sub_keys: list[int], rounds: int):

    dec_sub_keys = []

    for i in range(rounds + 1):
        dec_sub_keys = sub_keys[4*i: (4*i + 4)] + dec_sub_keys

    #rodada 0
    state = add_round_key(block, dec_sub_keys[0:4])

    for round in range(rounds):
        if round + 1 < rounds:
            state = dec_block_round(state, dec_sub_keys[(4*round + 4): (4*round + 8)])
        else:
            #última rodada
            state = add_round_key(dec_byte_sub(dec_shift_row(state)),dec_sub_keys[(4*round + 4): (4*round + 8)])

    return state

#decripta uma rodada do AES
def dec_block_round(state: list[int], round_key: list[int]):

    return dec_mix_column(add_round_key(dec_byte_sub(dec_shift_row(state)), round_key))

def add_round_key(state: list[int], round_key: list[int]):
    new_state = []
    for i in range(4):
        new_state.append(state[i] ^ round_key[i])

    return new_state

#During encryption each value of the state is replaced with the corresponding SBOX value

def dec_byte_sub(state: list[int]):
    new_state = []
    for i in range(4):
        aux = 0
        for j in range(4):
            aux = aux + (REVERSED_SBOX[(state[i] & (0xFF << 8*j)) >> 8*j] << 8*j)
        new_state.append(aux)

    return new_state

#Arranges the state in a matrix and then performs a circular shift for each row. This is not a bit wise shift. The
#circular shift just moves each byte one space over. A byte that was in the second position may end up in the third
#position after the shift. The circular part of it specifies that the byte in the last position shifted one space will end up
#in the first position in the same row. 

def dec_shift_row(state: list[int]):
    state_matrix = gen_matriz(state)

    state_matrix[1] = [state_matrix[1][3]] + state_matrix[1][0:3]
    state_matrix[2] = state_matrix[2][2:] + state_matrix[2][0:2]
    state_matrix[3] = state_matrix[3][1:] + [state_matrix[3][0]]

    return reverse_gen_matriz(state_matrix)


def dec_mix_column(state: list[int]):
    mult_matrix = [ [0xE,0xB,0xD,0x9],
                    [0x9,0xE,0xB,0xD],
                    [0xD,0x9,0xE,0xB],
                    [0xB,0xD,0x9,0xE] ]
    
    state_matrix = gen_matriz(state)

    result_matrix = [[], [], [], []]

    for coluna in range(4):
        for linha in range(4):
            result_matrix[linha].append(
                    mul_galois(state_matrix[linha - linha][coluna], mult_matrix[linha][coluna - coluna]) ^
                    mul_galois(state_matrix[linha + 1 - linha][coluna], mult_matrix[linha][coluna + 1 - coluna]) ^
                    mul_galois(state_matrix[linha + 2 - linha][coluna], mult_matrix[linha][coluna + 2 - coluna]) ^
                    mul_galois(state_matrix[linha + 3 - linha][coluna], mult_matrix[linha][coluna + 3 - coluna])
            )
    result_matrix = reverse_gen_matriz(result_matrix)

    return result_matrix

def mul_galois(h: int, i: int):
    if(i == 1):
        return h
    if(h == 1):
        return i
    if(h == 0 or i == 0):
        return 0
    else:
        aux = L_TABLE[h] + L_TABLE[i]
        if aux > 0xFF:
            aux = aux - 0xFF

        return E_TABLE[aux]
    

def gen_matriz(state: list[int]):
    matrix = [[], [], [], []]

    for i in range(4):
        for j in range(4):
            if j == 0:
                aux = state[i] & 0xFF000000
                matrix[j].append(aux >> 24)
            elif j == 1:
                aux = state[i] & 0x00FF0000
                matrix[j].append(aux >> 16)
            elif j == 2:
                aux = state[i] & 0x0000FF00
                matrix[j].append(aux >> 8)
            elif j == 3:
                aux = state[i] & 0x000000FF
                matrix[j].append(aux)                  
    return matrix

def reverse_gen_matriz(matrix: list[list[int]]):
    new_state = [0x0, 0x0, 0x0, 0x0]

    for i in range(4):
        for j in range(4):
            if i == 0:
                new_state[j] = new_state[j] + (matrix[i][j] << 24)
            elif i == 1:
                new_state[j] = new_state[j] + (matrix[i][j] << 16)
            elif i == 2:
                new_state[j] = new_state[j] + (matrix[i][j] << 8)
            elif i == 3:
                new_state[j] = new_state[j] + matrix[i][j]

    return new_state


