# Little Endian

from collections.abc import ByteString
import hashlib

from table import K, shiftamount
from tool import *

# reference
# https://cs.indstate.edu/~fsagar/doc/paper.pdf


#Constants
A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476

BITPERBYTE = 8
GROUPLEN = 512  # bits
GROUPREMAIN = 448  # bits
WORDLEN = 32  # bits
WORDNUM = 16  # 16 words in one group
PADDINGLEN = GROUPLEN - GROUPREMAIN
OPERATIONNUM = 64  # 64 operations
OPERATIONROUND = 4  # 4 rounds


def md5_padding(obj, nbits):
    """
    >>> grouplen = 512
    >>> groupremain = 448
    >>> a = 0b11000
    >>> a <<= 1
    >>> bin(a)
    '0b110000'
    >>> a ^= 1
    >>> bin(a)
    '0b110001'
    >>> a <<= (groupremain - count_bit(a)) - 1
    >>> bin(a)
    '0b110001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    """
    obj = (obj << 1) ^ 1
    obj = (obj << (nbits - 1))
    return obj


def md5_prepare(s):
    assert isinstance(s, ByteString)
    total_bitlen = bit_len = len(s) * BITPERBYTE
    remainder = bit_len % GROUPLEN
    s = int.from_bytes(s, "big")
    if remainder != GROUPREMAIN:
        # Need to padding bits
        # first bit is 1
        # then padding bit 0 until if passes
        if remainder > GROUPREMAIN:
            padding_len = (GROUPLEN - remainder) + GROUPREMAIN
        else:
            padding_len = GROUPREMAIN - remainder
        padded_s = md5_padding(s, padding_len)
    else:
        padded_s = s
    bit_len %= 2**64  # 64-bits length
    bit_len = reverse_int(bit_len, bytenum=8)
    padded_s = (padded_s << PADDINGLEN) + bit_len
    total_bitlen += padding_len
    return padded_s, total_bitlen


def md5_group(s, total_bitlen):
    """
    Split message s (after padded) into several 512-bits group, then split each group into 16 words of 32-bits
    """
    group_num = total_bitlen // GROUPLEN
    group_list = []
    group_fetch_int = bit_fetch(GROUPLEN)
    word_fetch_int = bit_fetch(WORDLEN)
    ind = 0
    while s:
        g = s & group_fetch_int
        group_list.append([0 for _ in range(WORDNUM)])
        word_ind = 0
        while g:
            word = g & word_fetch_int
            group_list[ind][WORDNUM - word_ind - 1] = reverse_int(word, bytenum=4)
            g >>= WORDLEN
            word_ind += 1
        s >>= GROUPLEN
        ind += 1
    return group_list, ind


def md5(group_list):
    """
    Calculate the MD5 of group
    """
    global A, B, C, D
    AA = A
    BB = B
    CC = C
    DD = D
    for group in group_list:
        for ind in range(OPERATIONNUM):
            if ind <= 15:
                F = aux_f(B, C, D)
                g = ind
            elif 16 <= ind <= 31:
                F = aux_g(B, C, D)
                g = (5 * ind + 1) % 16
            elif 32 <= ind <= 47:
                F = aux_h(B, C, D)
                g = (3 * ind + 5) % 16
            elif 48 <= ind <= 63:
                F = aux_i(B, C, D)
                g = (7 * ind) % 16
            dtemp = D
            D = C
            C = B
            B = modadd(B, leftrotate(modadd(A, F, K[ind], group[g]), shiftamount[ind]))
            A = dtemp
        AA = modadd(AA, A)
        BB = modadd(BB, B)
        CC = modadd(CC, C)
        DD = modadd(DD, D)
    output_list = [AA, BB, CC, DD]
    # Reverse each word
    for ind, word in enumerate(output_list):
        output_list[ind] = reverse_int(word)
    AA, BB, CC, DD = output_list
    return f"{AA:x}{BB:x}{CC:x}{DD:x}"
    

def main():
    # msg = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    msg = "hello world"
    msg_enc = msg.encode()
    prepared_msg, total_bitlen = md5_prepare(msg_enc)
    groups, group_num = md5_group(prepared_msg, total_bitlen)
    md5_msg = md5(groups)
    print(f"Calculated by this program: {md5_msg}")
    print(f"Calculated by hashlib.md5 : {hashlib.md5(msg_enc).hexdigest()}")
    print(md5_msg == hashlib.md5(msg_enc).hexdigest())


main()

