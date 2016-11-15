from __future__ import division, absolute_import, print_function
from fractions import gcd
from random import randrange
from collections import namedtuple
from math import log

binary_type = str
range_func = xrange

#key generation
def check_prime(n, k=30):
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

def rand_prime(n=10 ** 8):
    p = 1
    while not check_prime(p):
        p = randrange(n)
    return p

def multiplicative_inverse(modulus, value):
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

Key_pair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')

def generation_key_pair(n, public=None):
    prime1 = rand_prime(n)
    prime2 = rand_prime(n)
    composite = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)

    if public is None:
        private = None
        while True:
            private = randrange(totient)
            if gcd(private, totient) == 1:
                break
        public = multiplicative_inverse(totient, private)

    else:
        private = multiplicative_inverse(totient, public)

    assert public * private % totient == gcd(public, totient) == gcd(private, totient) == 1
    assert pow(pow(1234567, public, composite), private, composite) == 1234567
    return Key_pair(Key(public, composite), Key(private, composite))


def key_to_str(key):
    return ':'.join((('%%0%dx' % ((int(log(number, 256)) + 1) * 2)) % number) for number in key)

def str_to_key(keystr):
    return Key(*(int(number, 16) for number in keystr.split(':')))


if __name__ == '__main__':
    t1, t2 = generation_key_pair(2 ** 256)
    print (type(t1))