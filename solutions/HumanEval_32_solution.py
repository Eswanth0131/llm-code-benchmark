def poly(xs: list, x: float) -> float:
    return sum(coeff * (x ** i) for i, coeff in enumerate(xs))

def find_zero(xs: list) -> float:
    left, right = -1e6, 1e6
    while right - left > 1e-7:
        mid = (left + right) / 2
        val = poly(xs, mid)
        if abs(val) < 1e-7:
            return mid
        elif val > 0:
            right = mid
        else:
            left = mid
    return (left + right) / 2
