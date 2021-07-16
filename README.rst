===============================
Implementation of MD5 algorithm
===============================

---------------------
HOWTO
---------------------

i. Modify the message that is needed to be hash in ``main`` function in ``main.py``

::

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
#. Record the bit length of ``obj``.
    ::

        bitlen = len(obj) * 8  # 8 bits per byte

#. Padding the message as follows:  
    a. Padding a ``1`` at the end of the ``obj``.
    ::
        
        obj = (obj << 1) + 1
    b. Padding n ``0`` at the end of the ``obj``.


---------------------
REFERENCE
---------------------

`https://cs.indstate.edu/~fsagar/doc/paper.pdf<https://cs.indstate.edu/~fsagar/doc/paper.pdf>`_

