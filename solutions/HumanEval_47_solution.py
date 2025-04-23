def median(l: list) -> float:
    l_sorted = sorted(l)
    n = len(l_sorted)
    mid = n // 2
    if n % 2 == 0:
        return (l_sorted[mid - 1] + l_sorted[mid]) / 2
    else:
        return l_sorted[mid]
