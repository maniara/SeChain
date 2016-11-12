from ecdsa import SigningKey, NIST256p, VerifyingKey

def generate_key():
    sk = SigningKey.generate(curve=NIST256p)
    sk_string = sk.to_string()
    vk = sk.get_verifying_key()
    vk_string = vk.to_string()
    sk2 = SigningKey.from_string(sk_string, curve=NIST256p)

    print ''.join(x.encode('hex') for x in sk_string)
    print ''.join(x.encode('hex') for x in vk_string)
