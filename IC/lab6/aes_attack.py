from math import ceil
import base64
import os
from random import randint
from Crypto.Cipher import AES
from utils import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
backend = default_backend()


def split_bytes_in_blocks(x, block_size):
    nb_blocks = ceil(len(x)/block_size)
    return [x[block_size*i:block_size*(i+1)] for i in range(nb_blocks)]


def pkcs7_padding(message, block_size):
    padding_length = block_size - (len(message) % block_size)
    if padding_length == 0:
        padding_length = block_size
    padding = bytes([padding_length]) * padding_length
    return message + padding


def pkcs7_strip(data):
    padding_length = data[-1]
    return data[:- padding_length]


def encrypt_aes_128_ecb(msg, key):
    padded_msg = pkcs7_padding(msg, block_size=16)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(padded_msg) + encryptor.finalize()


def decrypt_aes_128_ecb(ctxt, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ctxt) + decryptor.finalize()
    message = pkcs7_strip(decrypted_data)
    return message

# You are not suppose to see this


class Oracle:
    def __init__(self):
        self.key = 'Mambo NumberFive'.encode()
        self.prefix = 'PREF'.encode()
        self.target = base64.b64decode(  # You are suppose to break this
            "RG8gbm90IGxheSB1cCBmb3IgeW91cnNlbHZlcyB0cmVhc3VyZXMgb24gZWFydGgsIHdoZXJlIG1vdGggYW5kIHJ1c3QgZGVzdHJveSBhbmQgd2hlcmUgdGhpZXZlcyBicmVhayBpbiBhbmQgc3RlYWwsCmJ1dCBsYXkgdXAgZm9yIHlvdXJzZWx2ZXMgdHJlYXN1cmVzIGluIGhlYXZlbiwgd2hlcmUgbmVpdGhlciBtb3RoIG5vciBydXN0IGRlc3Ryb3lzIGFuZCB3aGVyZSB0aGlldmVzIGRvIG5vdCBicmVhayBpbiBhbmQgc3RlYWwuCkZvciB3aGVyZSB5b3VyIHRyZWFzdXJlIGlzLCB0aGVyZSB5b3VyIGhlYXJ0IHdpbGwgYmUgYWxzby4="
        )


    def encrypt(self, message):
        return encrypt_aes_128_ecb(
            self.prefix + message + self.target,
            self.key
        )

# Task 1


def findBlockSize():
    initialLength = len(Oracle().encrypt(b''))
    i = 0
    while 1:  # Feed identical bytes of your-string to the function 1 at a time until you get the block length
        # You will also need to determine here the size of fixed prefix + target + pad
        # And the minimum size of the plaintext to make a new block
        length = len(Oracle().encrypt(b'X'*i))

        if length != initialLength:
            block_size = length - initialLength
            sizeOfTheFixedPrefixPlusTarget = initialLength - i
            minimumSizeToAlighPlaintext = i
            return block_size, sizeOfTheFixedPrefixPlusTarget, minimumSizeToAlighPlaintext

        i += 1


# Task 2


def findPrefixSize(block_size):
    # Bruteforce prefix pad such that we find "penguins" in the encrypted blocks
    
    RANDOM = 4
    for left_pad in range(block_size):
        ct = Oracle().encrypt((left_pad + block_size * RANDOM) * b'X')
        blocks = split_bytes_in_blocks(ct, block_size)

        for j in range(len(blocks) - RANDOM + 1):
            if blocks[j] == blocks[j + 1] == blocks[j + 2] == blocks[j + 3]:
                return block_size * j - left_pad

    return 0


# Task 3
def recoverOneByteAtATime(block_size, prefix_size, target_size):
    known_target_bytes = b""

    for _ in range(target_size):
        # prefix_size + padding_length + known_len + 1 = 0 mod block_size

        # target block plaintext contains only known characters except its last character
        # Don't forget to use split_bytes_in_blocks to get the correct block

        # trying every possibility for the last character

        known_len = len(known_target_bytes)
        padding_length = (- known_len - 1 - prefix_size) % block_size
        padding = b"X" * padding_length


        start = ((prefix_size + known_len) // block_size) * block_size
        stop = ((prefix_size + known_len) // block_size + 1) * block_size
        target_block = Oracle().encrypt(padding)[start:stop]

        for i in range(256):
            msg = padding + known_target_bytes + bytes([i])
            block = Oracle().encrypt(msg)[start:stop]
            if block == target_block:
                known_target_bytes += bytes([i])
                break

    print(known_target_bytes.decode())


# Find block size, prefix size, and length of plaintext size to allign blocks
block_size, sizeOfTheFixedPrefixPlusTarget, minimumSizeToAlignPlaintext = findBlockSize()
print("Block size:\t\t\t" + str(block_size))
print("Size of prefix and target:\t" + str(sizeOfTheFixedPrefixPlusTarget))
print("Pad needed to align:\t\t" + str(minimumSizeToAlignPlaintext))

# Find size of the prefix
prefix_size = findPrefixSize(block_size)
print("\nPrefix Size:\t" + str(prefix_size))

# Size of the target
target_size = sizeOfTheFixedPrefixPlusTarget - \
    minimumSizeToAlignPlaintext - prefix_size

print("\nTarget:")
recoverOneByteAtATime(block_size, prefix_size, target_size)
