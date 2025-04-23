def starts_one_ends(n: int) -> int:
    if n == 1:
        return 1  # Only number is 1
    return 9 * (10 ** (n - 2)) * 2 - (10 ** (n - 2))
