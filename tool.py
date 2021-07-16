from numbers import Integral
import struct

# Auxiliary Functions
# F(B, C, D) = (B ∧ C) ∨ (¬B ∧ D)
# G(B, C, D) = (B ∧ D) ∨ (C ∧ ¬D)
# H(B, C, D) = B ⊕ C ⊕ D
# I(B, C, D) = C ⊕ (B ∨ ¬D)

def aux_f(b, c, d):
    return (b & c) | ((~b) & d)

def aux_g(b, c, d):
    return (b & d) | (c & (~d))

def aux_h(b, c, d):
    return b ^ c ^ d

def aux_i(b, c, d):
    return c ^ (b | (~d))

def reverse_int(integer, bytenum=4):
    """
    Reverse the byte order of integer 

    >>> a = 1 + 2**(4 * 8)  # 4-byte integer plus one
    >>> hex(a)
    '0x100000001'
    >>> a = reverse_int(a, bytenum=4)
    >>> hex(a)
    '0x01000010'
    """
    assert isinstance(integer, Integral)
    fmt = {
        4: "I", # 4-byte unsigned int
        8: "Q", # 8-byte unsigned int
    }[bytenum]
    return struct.unpack(f">{fmt}", struct.pack(f"<{fmt}", integer))[0]

def modadd(a, *args):
    for v in args:
        a += v
        a %= (2**32)
    return a


def leftrotate(obj, length):
    return (obj << length) | (obj >> (32 - length))


def bit_fetch(num):
    return (1 << num) - 1


def count_bit(obj):
    num = 0
    while obj:
        obj >>= 1
        num += 1
    return num

