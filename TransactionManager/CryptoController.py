#-*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function
from base64 import b64encode
from fractions import gcd
from random import randrange
from collections import namedtuple
from math import log
from binascii import hexlify, unhexlify


binary_type = str
range_func = xrange

def checkPrime(n, k=30):
    if n <= 3:
        return n == 2 or n == 3
    neg_one = n - 1

    s, d = 0, neg_one
    while not d & 1:
        s, d = s + 1, d >> 1
    assert 2 ** s * d == neg_one and d & 1

    for _ in range_func(k):
        a = randrange(2, neg_one)
        x = pow(a, d, n)
        if x in (1, neg_one):
            continue
        for _ in range_func(s - 1):
            x = x ** 2 % n
            if x == 1:
                return False
            if x == neg_one:
                break
        else:
            return False
    return True


def randPrime(n=10 ** 8):
    p = 1
    while not checkPrime(p):
        p = randrange(n)
    return p


def multiplicativeInv(modulus, value):
    x, lastx = 0, 1
    a, b = modulus, value

    while b:
        a, q, b = b, a // b, a % b
        x, lastx = lastx - q * x, x
    result = (1 - lastx * modulus) // value

    if result < 0:
        result += modulus
    assert 0 <= result < modulus and value * result % modulus == 1
    return result

KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')

# Blockchain
# encrypt with private key

def data_encode(msg, privateKey, verbose=False):
    chunkSize = int(log(privateKey['modulus'], 256))
    outChunk = chunkSize + 1
    outFmt = '%%0%dx' % (outChunk * 2, )

    bMsg = msg if isinstance(msg, binary_type) else msg.encode('utf-8')
    result = []

    for start in range_func(0, len(bMsg), chunkSize):
        chunk = bMsg[start:start + chunkSize]
        chunk += b'\x00' * (chunkSize - len(chunk))
        plain = int(hexlify(chunk), 16)
        coded = pow(plain, privateKey['exponent'], privateKey['modulus'])
        bcoded = unhexlify((outFmt % coded).encode())
        if verbose:
            print('Encode: ', chunkSize, chunk, plain, coded, bcoded)
        result.append(bcoded)

    return b''.join(result)


def data_decode(bcipher, publicKey, verbose=False):
    chunkSize = int(log(publicKey['modulus'], 256))
    outChunk = chunkSize + 1
    outFmt = '%%0%dx' % (chunkSize * 2, )
    result = []

    for start in range_func(0, len(bcipher), outChunk):
        bcoded = bcipher[start: start + outChunk]
        coded = int(hexlify(bcoded), 16)
        plain = pow(coded, publicKey['exponent'], publicKey['modulus'])
        mask = (1 << (chunkSize * 8)) - 1
        plain &= mask
        chunk = unhexlify((outFmt % plain).encode())

        if verbose:
            print('Encode: ', chunkSize, chunk, plain, coded, bcoded)
        result.append(chunk)
    return b''.join(result).rstrip(b'\x00').decode('utf-8')

def keyTostr(key):
    return ':'.join((('%%0%dx' % ((int(log(number, 256)) + 1) * 2)) % number) for number in key)

def strTokey(keyStr):
    return Key(*(int(number, 16) for number in keyStr.split(':')))

#
# def main():
#     pubkey, privkey = keyGeneration(2 ** 256)
#     msg = 'Blockchain is a osdkfpsdifpi'
#     h = dataEncode(msg, privkey, True)
#     p = dataDecode(h, pubkey, True)
#     print('-' * 20)
#     print('message:', msg)
#     print('encoded:', b64encode(h).decode())
#     print('decoded:', p)
#     print('private key:', keyTostr(privkey))
#     print('public key:', keyTostr(pubkey))
# if __name__ == '__main__':
#     main()

