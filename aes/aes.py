# coding: utf-8

import numpy as np
from .sbox import Sbox, InvSbox, Rcon
from .sbox import M1, M2, M3, M9, M11, M13, M14
from base64 import urlsafe_b64encode as b64encode
from base64 import urlsafe_b64decode as b64decode

StateSlice = [-1, 4, 4]


def text2states(text):
    if isinstance(text, str):
        text = text.encode()
    elif isinstance(text, (bytes, np.ndarray)):
        pass
    else:
        raise TypeError("Type of input text", type(text), "is not supported.")

    s0 = np.array(list(text))
    rest = (16 - (len(s0) % 16)) % 16
    s1 = np.r_[s0, np.zeros(rest)]
    s2 = s1.reshape(StateSlice)
    return s2.astype(np.int8)


def states2text(state):
    s0 = state.ravel()
    s1 = s0.tostring()
    return s1.rstrip(b"\0")


def subBytes(state):
    return np.take(Sbox, state)


def invSubBytes(state):
    return np.take(InvSbox, state)


def rShiftRows(state):
    for i in range(4):
        state[:, i, :] = np.roll(state[:, i, :], i)
    return state


def lShiftRows(state):
    for i in range(4):
        state[:, i, :] = np.roll(state[:, i, :], -i)
    return state


def _mixColumn(a):
    # https://en.wikipedia.org/wiki/Rijndael_MixColumns#Implementation_example
    xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)
    b = list(map(xtime, a))
    r = np.zeros(4, dtype=np.int8)
    r[0] = b[0] ^ a[3] ^ a[2] ^ b[1] ^ a[1]
    r[1] = b[1] ^ a[0] ^ a[3] ^ b[2] ^ a[2]
    r[2] = b[2] ^ a[1] ^ a[0] ^ b[3] ^ a[3]
    r[3] = b[3] ^ a[2] ^ a[1] ^ b[0] ^ a[0]
    return r


def _mixColumnByTable(a):
    b0, b1, b2, b3 = a
    d = np.zeros(4, dtype=np.int8)
    d[0] = M2[b0] ^ M3[b1] ^ M1[b2] ^ M1[b3]
    d[1] = M1[b0] ^ M2[b1] ^ M3[b2] ^ M1[b3]
    d[2] = M1[b0] ^ M1[b1] ^ M2[b2] ^ M3[b3]
    d[3] = M3[b0] ^ M1[b1] ^ M1[b2] ^ M2[b3]
    return d


def _invMixColumnByTable(a):
    b0, b1, b2, b3 = a
    d = np.zeros(4, dtype=np.int8)
    d[0] = M14[b0] ^ M11[b1] ^ M13[b2] ^ M9[b3]
    d[1] = M9[b0] ^ M14[b1] ^ M11[b2] ^ M13[b3]
    d[2] = M13[b0] ^ M9[b1] ^ M14[b2] ^ M11[b3]
    d[3] = M11[b0] ^ M13[b1] ^ M9[b2] ^ M14[b3]
    return d


def mixColumn(state):
    s0 = state.transpose([0, 2, 1]).reshape((-1, 4))
    s1 = np.apply_along_axis(_mixColumnByTable, 1, s0)
    s2 = s1.reshape([-1, 4, 4]).transpose([0, 2, 1])
    return s2


def invMixColumn(state):
    s0 = state.transpose([0, 2, 1]).reshape((-1, 4))
    s1 = np.apply_along_axis(_invMixColumnByTable, 1, s0)
    s2 = s1.reshape([-1, 4, 4]).transpose([0, 2, 1])
    return s2


def keySchedule(key):
    if len(key) != 16:
        raise ValueError("Only key with 16 byte length supported!")

    r0 = text2states(key).reshape((4, 4)).tolist()
    for i in range(4, 4 * 11):
        r0.append([])

        if i % 4 == 0:
            byte = r0[i - 4][0] ^ Sbox[r0[i - 1][1]] ^ Rcon[i // 4]
            r0[i].append(byte)

            for j in range(1, 4):
                byte = r0[i - 4][j] ^ Sbox[r0[i - 1][(j + 1) % 4]]
                r0[i].append(byte)
        else:
            for j in range(4):
                byte = r0[i - 4][j] ^ r0[i - 1][j]
                r0[i].append(byte)
    return np.array(r0).reshape((-1, 4, 4))


def addRoundKey(state, key):
    return np.bitwise_xor(state, key)


def aes_encrypt(data, key):
    roundKey = keySchedule(key)
    state = text2states(data)
    s0 = addRoundKey(state, roundKey[0])
    for i in range(1, 11):
        s1 = subBytes(s0)
        s2 = lShiftRows(s1)
        s3 = mixColumn(s2) if i != 10 else s2
        s0 = addRoundKey(s3, roundKey[i])
    s4 = s0.ravel().astype(np.int8)
    b0 = s4.tobytes()
    b1 = b64encode(b0)

    return b1


def aes_decrypt(b1, key):
    roundKey = keySchedule(key)

    b0 = b64decode(b1)
    s4 = np.frombuffer(b0, dtype=np.int8)
    s0 = s4.reshape([-1, 4, 4])
    for i in reversed(range(1, 11)):
        s3 = addRoundKey(s0, roundKey[i])
        s2 = invMixColumn(s3) if i != 10 else s3
        s1 = rShiftRows(s2)
        s0 = invSubBytes(s1)

    state = addRoundKey(s0, roundKey[0])
    text = states2text(state.astype(np.int8))

    return text


def testAll():
    # Testing
    Test_key = "Thats my Kung Fu"
    Test_text = b"""    The quick brown fox jumps over the lazy dog.
    %75319024 &[{}(=*)+]
    """
    encoded_state = text2states(Test_text)
    decoded_text = states2text(encoded_state)
    assert decoded_text == Test_text

    roundKey = keySchedule(Test_key)
    assert roundKey.shape == (11, 4, 4)

    temp_state = addRoundKey(encoded_state, roundKey[0])
    decoded_state = addRoundKey(temp_state, roundKey[0])
    assert (decoded_state == encoded_state).all()

    temp_state = mixColumn(encoded_state)
    decoded_state = invMixColumn(temp_state)
    assert (decoded_state == encoded_state).all()

    temp_state = lShiftRows(encoded_state)
    decoded_state = rShiftRows(temp_state)
    assert (decoded_state == encoded_state).all()
