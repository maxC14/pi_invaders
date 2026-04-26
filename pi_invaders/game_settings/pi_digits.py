import mpmath


_PRECISION_BUFFER = 8
_cached_digits = ""


def get_pi_digit(index):
    return get_pi_digits(index + 1)[index]


def get_pi_digits(count):
    global _cached_digits

    if count < 1:
        return ""

    if len(_cached_digits) < count:
        mpmath.mp.dps = count + _PRECISION_BUFFER
        _cached_digits = str(mpmath.mp.pi).replace(".", "")[:count]

    return _cached_digits[:count]
