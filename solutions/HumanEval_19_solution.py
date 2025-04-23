def sort_numbers(numbers: str) -> str:
    word_to_digit = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
    }
    digit_to_word = {v: k for k, v in word_to_digit.items()}
    words = numbers.split()
    sorted_words = sorted(words, key=lambda w: word_to_digit[w])
    return ' '.join(sorted_words)
