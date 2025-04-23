def smallest_change(arr: list) -> int:
    count = 0
    n = len(arr)
    for i in range(n // 2):
        if arr[i] != arr[n - 1 - i]:
            count += 1
    return count
