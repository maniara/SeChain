from ecdsa import SigningKey, NIST256p, VerifyingKey
from ecdsa.util import PRNG
from SeChainController import Property


def get_seed():
    return Property.my_ip_address


def generate_pri_key():
    seed = get_seed()
    rng1 = PRNG(seed)
    sk = SigningKey.generate(entropy=rng1, curve=NIST256p)
    sk_string = sk.to_string()

    pri_key = ''.join(x.encode('hex') for x in sk_string)

    return pri_key, sk


def generate_pub_key(_pk):
    vk = _pk.get_verifying_key()
    vk_string = vk.to_string()

    pub_key = ''.join(x.encode('hex') for x in vk_string)

    return pub_key, vk


def perform_sha256(message):
    import hashlib

    hashed_msg = hashlib.sha256(message)
    hashed_dig = hashed_msg.hexdigest()

    return hashed_dig


'''
    2016/11/15
    module test
    need base58check encoding
'''
if __name__ == '__main__':
    import sys, hashlib
    sk1, sk2 = generate_pri_key()
    pk1, pk2 = generate_pub_key(sk2)
    hashed = perform_sha256(pk1)
    encoded = hashlib.new('ripemd160', hashed).hexdigest()
    version_added = "00"+encoded
    hashed1 = perform_sha256(version_added)
    hashed2 = perform_sha256(hashed1)

    address_before_encode = version_added + hashed2[:8]


    print sk1," ", sk2," ", sys.getsizeof(sk1)
    print pk1," ", pk2," ", sys.getsizeof(pk1)
    print hashed, " ", sys.getsizeof(hashed), " ", len(hashed)
    print encoded, " ", sys.getsizeof(encoded)," ", type(encoded), " ", len(encoded)
    print version_added
    print hashed2, " ", sys.getsizeof(hashed2), " ", len(hashed2)
    print "checksum is ", hashed2[:8]
    print address_before_encode
