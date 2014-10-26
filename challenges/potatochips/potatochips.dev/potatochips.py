#!/usr/bin/python
# Thank you for trying out our SHAREWARE text encoding product!
# Please use this script to encode and decode your messages!
# Glory be to the Dongerino!

# NOTE: A little corruption to the message is to be expected.
# This is by decree of the Great Dongerino for by his wisdom,
# Everything is Flawed.

import string

charset = "abcdefghijklmnopqrstuvwxyzABCDE"

def binary_stream(data):
    ret = map(int, "".join(map(lambda x: x[2:].rjust(8, '0'), map(bin, map(ord, data)))))
    return ret

def encode(data):
    length = len(data)
    stream = binary_stream(data) + [0]*(5 - ((length*8) % 5))
    blocks = [stream[i:i+5] for i in range(0, len(stream), 5)]
    binstr = ["".join(map(str, i)) for i in blocks]
    binint = [int(i, 2) for i in binstr]
    transf = [charset[i%30] for i in binint] 
    return "%d%s" % (length, "".join(transf))

def decode(data):
    counter = 0
    for i in range(len(data)):
        if data[i] in charset:
            break
        counter += 1
    length = int(data[:counter])
    datstr = data[counter:]
    datpos = [charset.index(i) for i in datstr]
    binstr = [bin(i)[2:].rjust(5, '0') for i in datpos]
    blocks = [map(int, i) for i in binstr]
    stream = [i for s in blocks for i in s]
    bytesb = [stream[i*8:i*8+8] for i in range(length)]
    bytesi = [int("".join(str(i) for i in j), 2) for j in bytesb]
    bytes  = [chr(i) for i in bytesi]
    return "".join(bytes)


