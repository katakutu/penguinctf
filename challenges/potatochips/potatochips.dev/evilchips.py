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

def encode(data, message):
    length = len(data)
    padding = (5 - ((length*8) % 5))
    print message[:padding]
    stream = binary_stream(data) + message[:padding]
    blocks = [stream[i:i+5] for i in range(0, len(stream), 5)]
    binstr = ["".join(map(str, i)) for i in blocks]
    binint = [int(i, 2) for i in binstr]
    transf = [charset[i%30] for i in binint] 
    return ("%d%s" % (length, "".join(transf)), padding)

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

def extract_hidden_line(data):
    counter = 0
    for i in range(len(data)):
        if data[i] in charset:
            break
        counter += 1
    length = int(data[:counter])
    padding = (5 - ((length*8) % 5))
    datstr = data[counter:]
    datpos = [charset.index(i) for i in datstr]
    binstr = [bin(i)[2:].rjust(5, '0') for i in datpos]
    blocks = [map(int, i) for i in binstr]
    stream = [i for s in blocks for i in s]
    return stream[-1*padding:]

def extract_hidden(lines):
    bits = []
    for i in lines:
        bits += extract_hidden_line(i) 
    chunks = [bits[i:i+8] for i in range(0, len(bits), 8)]
    letter = [int("".join(map(str, i)),2) for i in chunks]
    print "".join(map(chr, letter))

def available_space(messages):
    total = 0
    for i in messages:
        length = len(i)
        total += (5 - ((length*8) % 5))
    return total

def hide(data, messages):
    blob = binary_stream(data)
    print blob
    print "Need to hide %d bits" % len(blob)
    avai = available_space(messages)
    print "We have a space of %d bits over %d messages" % (avai, len(messages))
    if avai < len(blob):
        print "Not enough space to hide!"
        exit()
    print "Padding out %d bits" % (avai-len(blob))
    blob = blob + [0]*(avai-len(blob))
    print len(blob)
    potato = file("potato",'w')
    for i in messages:
        print "Converting line: %s" % i
        res = encode(i, blob)
        print res[0]
        blob = blob[res[1]:]
        print "%d bits left to hide" % len(blob)
        print
        potato.write(res[0]+"\n\n")


hide("flag{Penguin$LovePythonLists}", file("messages").read().split("\n"))
extract_hidden(file("potato").read().split("\n\n")[:-1])