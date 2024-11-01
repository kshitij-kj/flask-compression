# decompress.py

import ast

def remove_padding(padded_encoded_text):
    padding_info = padded_encoded_text[:8]
    extra_padding = int(padding_info, 2)
    encoded_text = padded_encoded_text[8:]  # Remove padding info bits
    return encoded_text[:-extra_padding]  # Remove extra padding

def decode_text(encoded_text, huffman_codes):
    current_code = ""
    decoded_text = ""
    reverse_huffman_codes = {code: char for char, code in huffman_codes.items()}

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_huffman_codes:
            character = reverse_huffman_codes[current_code]
            decoded_text += character
            current_code = ""
    
    return decoded_text

def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as file:
        # Read huffman_codes metadata
        codes_length = int.from_bytes(file.read(4), 'big')
        huffman_codes_str = file.read(codes_length).decode('utf-8')
        huffman_codes = ast.literal_eval(huffman_codes_str)

        # Read compressed data
        bit_string = ""
        byte = file.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

        # Decompress
        encoded_text = remove_padding(bit_string)
        decompressed_text = decode_text(encoded_text, huffman_codes)

        # Save output as .txt file
        with open(output_path, 'w') as output_file:
            output_file.write(decompressed_text)

    print("File decompressed successfully!")

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    decompress_file(input_file, output_file)
