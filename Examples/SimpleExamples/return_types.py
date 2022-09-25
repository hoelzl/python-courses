def int_sqrt_with_pair(n: int) -> tuple[int, str]:
    for m in range(n + 1):
        if m * m == n:
            return m, True
    return 0, ""


_m, _error = int_sqrt_with_pair(10)

x = _error + 1



