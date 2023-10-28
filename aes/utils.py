# padding of the message to be encrypted
def padding(message):

    if(len(message) % 16 == 0):
        remainder = 0
    else:
        remainder = 16 - len(message) % 16

    return message + ("X"*remainder)

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