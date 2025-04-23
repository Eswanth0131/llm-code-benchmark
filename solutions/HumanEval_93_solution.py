def encode(s: str) -> str:
    shift = 2 * 2  # equals 4
    result = []
    for char in s:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            rotated = chr((ord(char) - base + shift) % 26 + base)
            result.append(rotated)
        else:
            result.append(char)
    return ''.join(result)
