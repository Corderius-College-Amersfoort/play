def _clamp(num, min_, max_):
    if num < min_:
        return min_
    elif num > max_:
        return max_
    return num
