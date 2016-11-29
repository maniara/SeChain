from ecdsa import SigningKey, NIST256p, VerifyingKey, NIST192p
from ecdsa.util import PRNG, string_to_number
from SeChainController import Property
import binascii
'''
    key generation seed = ip address
'''


class keyPair():
    def __init__(self):
        self.private_key = generate_pri_key()[0]
        self.public_key = generate_pub_key(self.private_key)[0]


def get_seed():
    return Property.my_ip_address

'''
return (key hex string, key object)
'''
def generate_pri_key():
    seed = get_seed()
    rng1 = PRNG(seed)
    sk = SigningKey.generate(entropy=rng1, curve=NIST256p)
    sk_string = sk.to_string()

    sk_string_hex = binascii.hexlify(sk_string)

    return sk_string_hex, sk


'''
return (key hex string, key object)
'''
def generate_pub_key(_pk):

    # convert_pk = SigningKey.from_string(_pk, curve=NIST256p)
    _pk_unhex = binascii.unhexlify(_pk)
    secexp = string_to_number(_pk_unhex)
    origin_pk = SigningKey.from_secret_exponent(secexp, curve=NIST256p)

    vk = origin_pk.get_verifying_key()
    vk_string = vk.to_string()

    pub_key = binascii.hexlify(vk_string)

    return pub_key, vk


def perform_sha256(message):
    import hashlib

    hashed_msg = hashlib.sha256(message)
    hashed_dig = hashed_msg.hexdigest()

    return hashed_dig

'''
return address<string>
'''
def generate_address():
    import hashlib
    import base58

    sk1, sk2 = generate_pri_key()
    pk1, pk2 = generate_pub_key(sk1)
    hashed = perform_sha256(pk1)
    encoded = hashlib.new('ripemd160', hashed).hexdigest()
    version_added = "00" + encoded
    hashed1 = perform_sha256(version_added)
    hashed2 = perform_sha256(hashed1)

    address_before_encode = version_added + hashed2[:8]

    convert_address = str(bytearray.fromhex(address_before_encode))
    address_after_encode = base58.b58encode(convert_address)

    return address_after_encode



'''
    2016/11/15
    module test
'''
if __name__ == '__main__':
    import sys, hashlib
    import base58

    sk1, sk2 = generate_pri_key()
    pk1, pk2 = generate_pub_key(sk1)
    hashed = perform_sha256(pk1)
    encoded = hashlib.new('ripemd160', hashed).hexdigest()
    version_added = "00"+encoded
    hashed1 = perform_sha256(version_added)
    hashed2 = perform_sha256(hashed1)

    address_before_encode = version_added + hashed2[:8]

    convert_address = str(bytearray.fromhex(address_before_encode))
    address_after_encode = base58.b58encode(convert_address)

    msg = "msgtest"
    t = sk2.sign(msg)
    print t
    u = pk2.verify(t, msg)
    print u


    print "private KEY: ",sk1," ", sk2," ", sys.getsizeof(sk1), type(sk2)
    print "public KEY: ",pk1," ", pk2," ", sys.getsizeof(pk1), type(pk2)
    # print hashed, " ", sys.getsizeof(hashed), " ", len(hashed)
    # print encoded, " ", sys.getsizeof(encoded)," ", type(encoded), " ", len(encoded)
    # print version_added
    # print hashed2, " ", sys.getsizeof(hashed2), " ", len(hashed2)
    # print "checksum is ", hashed2[:8]
    #
    # print address_before_encode
    # print address_after_encode, type(address_after_encode)
    print generate_address()
    # t = generate_address()[0]
    # print t