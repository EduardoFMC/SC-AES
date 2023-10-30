#recebe um estado (lista de 4 inteiros de 4 bytes) e retorna uma matriz 4x4 com elementos de 1byte
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

#função inversa a gen_matriz: matriz -> estado
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

#recebe um nome de um arquivo e retorna uma lista com os bytes lidos
def prepare_mensage_ecb(arquivo):
    blocos = []

    with open(arquivo, "rb") as a:
        bytes = a.read()
        
        bytes = padding(bytes)
        
        for i in range(0, len(bytes), 4):
            blocos.append(int.from_bytes(bytes[i : i + 4], "big"))
        
        a.close()

    return blocos

#utilizado para debug
def print_estado(state: list[int]):
    new_state = []
    for i in range(4):
        new_state.append(hex(state[i]))
    print(new_state)

#recebe o nome do arquivo e o modo de operação ("cif" ou "dec") e retorna uma lista com os bytes do arquivo
def prepare_mensage_ctr(nomeArquivo, mode):
    blocks_16bytes = []

    with open(nomeArquivo, 'rb') as b:
        bytes = b.read()
        if mode == "cif":
            bytes = padding(bytes)

        for i in range(0, len(bytes), 16):
            blocks_16bytes.append(bytes[i: i + 16])
        b.close()
    
    return blocks_16bytes

#recebe 16 bytes e retorna uma lista de 4 interos
def ajeita_block_counter(bytes):
    list_int = []

    for i in range(0, 16, 4):
        list_int.append(int.from_bytes(bytes[i : i + 4], 'big'))
    
    return list_int

#le arquivo e retorna os seus bytes em uma lista
def dec_prepare_mensage_ecb(arquivo):
    blocos = []

    with open(arquivo, "rb") as a:
        bytes = a.read()

        for i in range(0, len(bytes), 4):
            blocos.append(int.from_bytes(bytes[i : i + 4], "big"))

        a.close()

    return blocos

# padding of the message to be encrypted
def padding(message_bytes):
    _16 = 16
    i = len(message_bytes) % 16
    i = 16 - i
    ret = message_bytes + i.to_bytes(1, 'big')*i

    return ret

# return a string separated ion blocks of 4 bytes in a list
def separate_into_blocks_of_4_bytes(key):
    key_bytes = bytes(key, 'utf-8')
    BLOCK_SIZE = 4
    blocks = [key_bytes[i:i+BLOCK_SIZE] for i in range(0, len(key_bytes), BLOCK_SIZE)]

    return blocks

# return a string separated ion blocks of 4 bytes in a list, but each block is a hex string
def separate_into_hex_blocks_of_4_bytes(key):
    key_bytes = bytes(key, 'utf-8')
    BLOCK_SIZE = 4
    blocks = [key_bytes[i:i+BLOCK_SIZE] for i in range(0, len(key_bytes), BLOCK_SIZE)]
    hex_blocks = [block.hex() for block in blocks]

    return hex_blocks

def string_to_hex_format(input_string):
    
    input_bytes = input_string.encode('utf-8')
    hex_string = ''.join([f"\\x{byte:02x}" for byte in input_bytes])
    
    return hex_string

def text_to_matrix(text):
    matrix = []
    for i in range(16):
        byte = (text >> (8 * (15 - i))) & 0xFF                      
        if i % 4 == 0:
            matrix.append([byte])                                   
        else:
            matrix[i // 4].append(byte)                             
    return matrix  

def xor(a, b):
    
    return [i ^ j for i, j in zip(a, b)]