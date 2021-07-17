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
    a. Padding a ``1`` at the end of the ``obj``.
    .. code-block::python

        obj = (obj << 1) + 1
    b. Padding n ``0`` at the end of the ``obj``. 
    .. code-block::python

        obj = (obj << (448 - bitlen - 1) % 512
    c. Add the bit length (little-endian) of original message
    .. code-block::python

        bitlen = reverse_int(bitlen, bytenum=8) 
        padded_s = (padded << 64) + bitlen

iv. Split message into groups, each of which consists of 16 words of 32-bits long (Each word is little-endian).
    .. code-block::python

        group_list[group_ind][word_ind] = reverse_int(group & 0xFFFFFFFF, bytenum=4)
        group >>= 32

v. Calculate MD5. 4 rounds, each of which has 16 operations.
vi. Append the output 4 words ``AA, BB, CC, DD``.


---------------------
REFERENCE
---------------------

`https://cs.indstate.edu/~fsagar/doc/paper.pdf<https://cs.indstate.edu/~fsagar/doc/paper.pdf>`_

