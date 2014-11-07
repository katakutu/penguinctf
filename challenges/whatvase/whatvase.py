#!/usr/bin/python
# Serve with socat -T 30 TCP-LISTEN:34123,fork EXEC:./whatvase.py

import base64
import random
import sys

BLOCK_SIZE = 64 # Has to be multiple of 8

def crypto_encrypt(key_bits, iv_bits, msg_bits):
    # Super secure CBC mode cipher!
    msg_chunks = [msg_bits[i:i+BLOCK_SIZE] for i in range(0, len(msg_bits), BLOCK_SIZE)]
    computed_chunk = iv_bits
    encrypted_bits = []
    for plaintext_chunk in msg_chunks:
        computing_chunk  = []
        encrypting_chunk = []
        for i in range(BLOCK_SIZE):
            computing_chunk.append(plaintext_chunk[i]^computed_chunk[i])
            encrypting_chunk.append(computing_chunk[i]^key_bits[i])
        computed_chunk = encrypting_chunk
        encrypted_bits = encrypted_bits + computed_chunk
    return encrypted_bits

def crypto_decrypt(key_bits, iv_bits, msg_bits):
    msg_chunks = [msg_bits[i:i+BLOCK_SIZE] for i in range(0, len(msg_bits), BLOCK_SIZE)]
    computed_chunk = iv_bits
    plaintext_bits = []
    for ciphertext_chunk in msg_chunks:
        computing_chunk = []
        for i in range(BLOCK_SIZE):
            computing_chunk.append(ciphertext_chunk[i]^key_bits[i])
            plaintext_bits.append(computing_chunk[i]^computed_chunk[i])
        computed_chunk = ciphertext_chunk

    return plaintext_bits

def number_to_bits(number):
    bin_number = bin(number)[2:]
    bit_string = "%s%s" % ("" if len(bin_number) % 2 == 0 else "0", bin_number)
    return [int(i) for i in bit_string]

def pad_bit_stream(bit_stream, total_len):
    # Pad out the bit stream by prepending null bits
    bits = list(bit_stream)
    bits = [0]*(total_len-len(bits)) + bits 
    return bits

def bits_to_bytes(bit_stream):
    byte_chunks = [bit_stream[i:i+8] for i in range(0, len(bit_stream), 8)]
    bytes = ""
    for i in byte_chunks:
        byte = int("".join(map(str, i)), 2)
        bytes += chr(byte)
    return bytes

def bytes_to_bits(bytes):
    bit_stream = []
    for i in bytes:
        bits = pad_bit_stream(bin(ord(i))[2:], 8)
        for j in bits:
            bit_stream.append(int(j))
    return bit_stream

def encrypt():
    # Get key
    key = int(r_msg("Please provide your key (64 bits in hexadecimal): "), 16)
    if key > 0xffffffffffffffff:
        w_msg("Keep your keys smaller than 64 bits!")
        exit(0)

    # Generate IV 
    iv  = random.getrandbits(BLOCK_SIZE)
    w_msg("Generated the following IV: %x" % iv)

    # Get msg
    msg = r_msg("Please provide your message to encrypt: ")

    # Convert the key and iv to bits
    key_bits = number_to_bits(key)
    key_bits = pad_bit_stream(key_bits, BLOCK_SIZE)
    iv_bits  = number_to_bits(iv)
    iv_bits  = pad_bit_stream(iv_bits, BLOCK_SIZE)

    # Pad out the message to fit BLOCK_SIZE
    block_size_in_bytes = BLOCK_SIZE / 8
    bytes_to_pad = block_size_in_bytes - (len(msg) % block_size_in_bytes)
    msg = msg + chr(bytes_to_pad)*bytes_to_pad # PKCS #5 Padding

    # Convert the message to bits
    hex_msg  = int(msg.encode("hex"), 16)
    msg_bits = number_to_bits(hex_msg)

    cipherbits = crypto_encrypt(key_bits, iv_bits, msg_bits)
    ciphertext = base64.encodestring(bits_to_bytes(cipherbits)).replace("\n", "")
    ciphertext = "%x:%s" % (iv, ciphertext)
    return ciphertext

def decrypt(key=None):
    # Get key
    if key == None:
        key = int(r_msg("Please provide your key (64 bits in hexadecimal): "), 16)
    if key > 0xffffffffffffffff:
        w_msg("Keep your keys smaller than 64 bits!")
        exit(0) 

    # Get ciphertext
    ciphertext  = r_msg("Please provide your encrypted text: ")
    crypt_parts = ciphertext.split(":")
    if len(crypt_parts) != 2:
        w_msg("Invalid ciphertext format.")
        exit(0)
    enc = base64.decodestring(crypt_parts[1])
    if len(enc) % 8 != 0:
        w_msg("Invalid ciphertext length")
        exit(0)

    # Get iv
    iv = int(crypt_parts[0], 16)
    w_msg("Found the following IV: %x" % iv)

    # Convert the key and iv to bits
    key_bits = number_to_bits(key)
    key_bits = pad_bit_stream(key_bits, BLOCK_SIZE)
    iv_bits  = number_to_bits(iv)
    iv_bits  = pad_bit_stream(iv_bits, BLOCK_SIZE)  
    
    # Convert the encrypted bytes to bits
    enc_bits = bytes_to_bits(enc)

    # Decrypt and Convert the bits back to ascii
    plaintext_bits = crypto_decrypt(key_bits, iv_bits, enc_bits)
    byte_chunks = [plaintext_bits[i:i+8] for i in range(0, len(plaintext_bits), 8)]
    plaintext = ""
    for i in byte_chunks:
        plaintext += chr(int("".join(map(str, i)), 2))
    
    # Check and remove the padding before returning plaintext
    padding_len = ord(plaintext[-1])
    padding     = plaintext[-1*padding_len:]
    for i in padding:
        if ord(i) != padding_len:
            w_msg("Invalid padding")
            exit(0)
    plaintext = plaintext[:-1*padding_len]
    return plaintext

def admin_debug():
    # admin.key has format <key>:<password>
    admin = file('admin.key').read().split(":")
    plaintext = decrypt(int(admin[0], 16))
    password = r_msg("Please enter the admin password: ")
    if password.strip() == admin[1].strip():
        w_msg("Here is the decrypted admin information: %s" % plaintext)
    else:
        w_msg("That admin password is incorrect.")


def serve():
    w_msg("Welcome to the WhatVase? Crypto Service.")
    w_msg("We provide encryption and decryption services for you! Free of charge!")
    w_msg("We'd ask you to sit down, but you're not going to anyway. Don't worry about the vase.")
    w_msg("----------------------------------------------------------------------")
    w_msg("1. Encrypt\n2. Decrypt\n\nYour choice: ")

    choice = r_msg()
    if choice == "1":
        ciphertext = encrypt()
        w_msg("Here's your ciphertext: %s" % ciphertext)
    elif choice == "2":
        plaintext = decrypt()
        w_msg("Here's your plaintext: %s" % plaintext)
    elif choice == "3":
        # For on-site debugging of generated admin system failure reports
        remote_admin_debug = admin_debug() 
    else:
        w_msg("That's not a valid choice! Exiting!")
        exit(0)

    w_msg("Thank you for choosing WhatVase?")

def w_msg(message, newline=True):
    sys.stdout.write(message)
    if newline:
        sys.stdout.write("\n")
    sys.stdout.flush()

def r_msg(message=None):
    if message:
        w_msg(message, newline=False)
    data = sys.stdin.readline().strip()
    return data
def main():
    serve()

if __name__ == "__main__":
    main()