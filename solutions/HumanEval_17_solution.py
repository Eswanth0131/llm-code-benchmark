def parse_music(music_string: str) -> list[int]:
    notes = music_string.split()
    result = []
    for note in notes:
        if note == 'o':
            result.append(4)
        elif note == 'o|':
            result.append(2)
        elif note == '.|':
            result.append(1)
    return result
