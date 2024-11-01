# compress.py

import heapq
import os
from collections import defaultdict, Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_dict(text):
    return Counter(text)

def build_huffman_tree(frequency):
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def build_huffman_codes(node, code="", codes={}):
    if node:
        if node.char is not None:
            codes[node.char] = code
        build_huffman_codes(node.left, code + "0", codes)
        build_huffman_codes(node.right, code + "1", codes)
    return codes

def encode_text(text, huffman_codes):
    return ''.join(huffman_codes[char] for char in text)

def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    encoded_text = f"{encoded_text}{'0' * extra_padding}"
    padded_info = f"{extra_padding:08b}"
    return padded_info + encoded_text

def get_byte_array(padded_encoded_text):
    if len(padded_encoded_text) % 8 != 0:
        raise ValueError("Encoded text length is not a multiple of 8.")

    byte_array = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        byte_array.append(int(byte, 2))
    return byte_array

def compress_file(input_path, output_path):
    with open(input_path, 'r') as file:
        text = file.read()

    frequency = build_frequency_dict(text)
    huffman_tree = build_huffman_tree(frequency)
    huffman_codes = build_huffman_codes(huffman_tree)

    encoded_text = encode_text(text, huffman_codes)
    padded_encoded_text = pad_encoded_text(encoded_text)
    byte_array = get_byte_array(padded_encoded_text)

    # Save compressed file with codes
    with open(output_path, 'wb') as output:
        # Store huffman_codes as metadata
        huffman_codes_str = str(huffman_codes).encode('utf-8')
        output.write(len(huffman_codes_str).to_bytes(4, 'big'))  # Write length of codes
        output.write(huffman_codes_str)  # Write codes
        output.write(byte_array)  # Write encoded data

    print("File compressed successfully!")

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    compress_file(input_file, output_file)
