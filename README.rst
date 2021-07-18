===============================
Implementation of MD5 algorithm
===============================

---------------------
HOWTO
---------------------

i. Modify the message that is needed to be hash in ``main`` function in ``main.py``
.. code-block::python

    msg = "hello world"

#. Run ``main.py`` and get the results

::

    Calculated by this program: 5eb63bbbe01eeed093cb22bb8f5acdc3
    Calculated by hashlib.md5 : 5eb63bbbe01eeed093cb22bb8f5acdc3
    True


---------------------
RATIONAL
---------------------

i. Encode the message into ``bytes`` object, named as ``obj``.

ii. Record the bit length of ``obj``.

    .. code-block::python

        bitlen = len(obj) * 8  # 8 bits per byte

iii. Padding the message as follows:  

    a. Calculate the total padding length that needed.
        .. code-block::python

            padding_len = (448 - bitlen) % 512
            if padding_len == 0:
                padding_len = 512  
                # If the original length (bitlen) equals to 448, then we need to 
                #   pad 512 bits
            total_bitlen = bitlen + padding_len

    b. Padding a ``1`` at the end of the ``obj``.
        .. code-block::python

            padded_s = (padded_s << 1) ^ 1
             
    c. Padding n ``0`` at the end of the ``obj``. 
        .. code-block::python

            padded_s = (padded_s << (padding_len - 1)
    d. Add the bit length (little-endian) of original message
        .. code-block::python

            bitlen = reverse_int(bitlen, bytenum=8) 
            padded_s = (padded_s << 64) + bitlen

iv. Split message into groups, each of which consists of 16 words of 32-bits long (Each word is little-endian).
    .. code-block::python

        # Initialize
        group_num, rem = divmod(total_bitlen, 512)
        if rem == 0:
            group_num -= 1
        group_list = [[0 for _ in range(16)] for __ in range(group_num)]
        group_ind = 0
        while padded_s:
            group = padded_s & 0xFFFF...FF   # 64 bytes
            word_ind = 0
            while group:
                group_list[group_ind][16 - word_ind - 1] = reverse_int(group & 0xFFFFFFFF, bytenum=4)
                group >>= 32
                word_ind += 1
            group_ind += 1
            padded_s >>= 512

v. Calculate MD5. 4 rounds, each of which has 16 operations, ref to ``md5`` function.
vi. Concatenate the output 4 words ``AA, BB, CC, DD``, need to add suffix ``0`` until each string is of 16 letters (8 bytes).
    .. code-block::python

        f"{AA:=08x}{BB:=08x}{CC:=08x}{DD:=08x}"


---------------------
REFERENCE
---------------------

https://cs.indstate.edu/~fsagar/doc/paper.pdf

