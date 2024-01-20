import random

random.seed(0)

def generate_number(number_width: str = "32-bit"):
    if number_width == "32-bit":
        return random.randint(0, 2**32 - 1)
    elif number_width == "64-bit":
        return random.randint(0, 2**64 - 1)
    else:
        raise ValueError("number_width must be either '32-bit' or '64-bit'")
    
def generate_array(array_length: int = 100, number_width: str = "32-bit"):
    return [generate_number(number_width) for _ in range(array_length)]

data = generate_array(array_length=100, number_width="32-bit")

def encode_to_varint_naive(number: int, varint_size: int = 8):
    if varint_size not in [4, 8, 16]:
        raise ValueError("varint_size must be either 4, 8 or 16")
    binary_representation = bin(number)[2:]
    reversed_binary_representation = binary_representation[::-1]
    chunk_size = varint_size - 1
    chunks = [reversed_binary_representation[i:i+chunk_size] for i in range(0, len(reversed_binary_representation), chunk_size)]
    # reverse the chunks
    chunks = [chunk[::-1] for chunk in chunks]
    # reverse the order of the chunks
    chunks = chunks[::-1]
    # left pad first chunk with zeros to make all chunks of equal size
    chunks[0] = chunks[0].zfill(chunk_size)
    # add 1 as the most significant bit to all chunks except the first one
    chunks = ["0" + chunk if i == 0 else "1" + chunk for i, chunk in enumerate(chunks)]
    # decode the chunks
    chunks = [int(chunk, 2) for chunk in chunks]
    return chunks

def decode_from_varint_naive(chunks: list[str], varint_size: int = 8):
    if varint_size not in [4, 8, 16]:
        raise ValueError("varint_size must be either 4, 8 or 16")
    # encode the chunks
    chunks = [bin(chunk)[2:] for chunk in chunks]
    # remove the most significant bit from all chunks except the first one
    chunks = [chunk[1:] if i != 0 else chunk for i, chunk in enumerate(chunks)]
    # reverse the order of the chunks
    chunks = chunks[::-1]
    # reverse the chunks
    chunks = [chunk[::-1] for chunk in chunks]
    # concatenate the chunks
    concatenated_chunks = "".join(chunks)
    # reverse the binary representation
    concatenated_chunks = concatenated_chunks[::-1]
    return int("".join(concatenated_chunks), 2)

if __name__ == "__main__":
    num = 292
    print("varint_size = 4")
    print("Original number:", num)
    encoded_num = encode_to_varint_naive(num, varint_size=4)
    print("Encoded number:", encoded_num)
    decoded_num = decode_from_varint_naive(encoded_num, varint_size=4)
    print("Decoded number:", decoded_num)
    print("")
    print("varint_size = 8")
    print("Original number:", num)
    encoded_num = encode_to_varint_naive(num, varint_size=8)
    print("Encoded number:", encoded_num)
    decoded_num = decode_from_varint_naive(encoded_num, varint_size=8)
    print("Decoded number:", decoded_num)
    print("")
    print("varint_size = 16")
    print("Original number:", num)
    encoded_num = encode_to_varint_naive(num, varint_size=16)
    print("Encoded number:", encoded_num)
    decoded_num = decode_from_varint_naive(encoded_num, varint_size=16)
    print("Decoded number:", decoded_num)