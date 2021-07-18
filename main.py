# Little Endian

from collections.abc import ByteString 
import hashlib

from table import K, shiftamount
from tool import *

# reference
# https://cs.indstate.edu/~fsagar/doc/paper.pdf


#Constants

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
    # if remainder != GROUPREMAIN:
    # Need to padding bits
    # first bit is 1
    # then padding bit 0 until total bit number is 448, modulo 512
    # 
    padding_len = (GROUPREMAIN - remainder) % GROUPLEN
    if padding_len == 0:
        padding_len = GROUPLEN
    padded_s = md5_padding(s, padding_len)
    bit_len %= 2**64  # 64-bits length
    bit_len = reverse_int(bit_len, bytenum=8)
    padded_s = (padded_s << PADDINGLEN) + bit_len
    total_bitlen += (padding_len + 64)
    return padded_s, total_bitlen


def md5_group(s, total_bitlen):
    """
    Split message s (after padded) into several 512-bits group, then split each group into 16 words of 32-bits
    """
    group_num, rem = divmod(total_bitlen, GROUPLEN)
    if rem == 0:
        group_num -= 1
    group_list = [[0 for _ in range(WORDNUM)] for __ in range(group_num + 1)]
    group_fetch_int = bit_fetch(GROUPLEN)
    word_fetch_int = bit_fetch(WORDLEN)
    ind = 0
    while s:
        g = s & group_fetch_int
        word_ind = 0
        while g:
            word = g & word_fetch_int
            group_list[group_num - ind][WORDNUM - word_ind - 1] = reverse_int(word, bytenum=4)
            g >>= WORDLEN
            word_ind += 1
        s >>= GROUPLEN
        ind += 1
    return group_list, ind


def md5(group_list):
    """
    Calculate the MD5 of group
    """
    AA = A = 0x67452301
    BB = B = 0xEFCDAB89
    CC = C = 0x98BADCFE
    DD = D = 0x10325476

    for group in group_list:
        A = AA
        B = BB
        C = CC
        D = DD
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
    return f"{AA:=08x}{BB:=08x}{CC:=08x}{DD:=08x}"  # Append zero before each byte to 8 characters
 

def main():
    msg = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    # msg = "hello world"
    # msg = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    msg_enc = msg.encode()
    prepared_msg, total_bitlen = md5_prepare(msg_enc)
    groups, group_num = md5_group(prepared_msg, total_bitlen)
    md5_msg = md5(groups)
    print(f"Calculated by this program: {md5_msg}")
    print(f"Calculated by hashlib.md5 : {hashlib.md5(msg_enc).hexdigest()}")
    print(md5_msg == hashlib.md5(msg_enc).hexdigest())


main()

