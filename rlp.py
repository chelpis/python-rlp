def RLP(x):
    assert _is_RLP_serializable(x)
    if type(x) is int and x >= 0:
        return RLP(BE(x))
    elif type(x) is bytes:
        return RLP_B(x)
    else:
        return RLP_L(x)


def _is_RLP_serializable(value):
    return (
        (type(value) is int and value >= 0)
        or type(value) is bytes
        or (
            type(value) is tuple
            and all(_is_RLP_serializable(v) for v in value)
        )
    )


def BE(n):
    assert type(n) is int and n >= 0
    byte_length = (n.bit_length() - 1) // 8 + 1
    return n.to_bytes(byte_length, "big")


def RLP_B(x):
    assert type(x) is bytes
    if len(x) == 1 and x[0] < 128:
        return x
        # 0 <= head <= 127
    elif len(x) < 56:
        return bytes([128 + len(x)]) + x
        # 0 <= len(x) <= 55
        # 128 <= head <= 183
    else:
        # 56 <= len(x) <= ...
        # 1 <= len(BE(len(x))) <= 8
        # 184 <= head <= 191
        return bytes([183 + len(BE(len(x)))]) + BE(len(x)) + x


def RLP_L(l):
    assert type(l) is tuple
    s = b"".join(RLP(e) for e in l)
    if len(s) < 56:
        # 0 <= len(s) <= 55
        # 192 <= head <= 247
        return bytes([192 + len(s)]) + s
    else:
        # 56 <= len(s) <= ...
        # 1 <= len(BE(len(s))) <= 9
        # 248 <= head <= 255
        return bytes([247 + len(BE(len(s)))]) + BE(len(s)) + s
