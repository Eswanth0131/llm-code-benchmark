def parse_nested_parens(paren_string: str) -> list[int]:
    groups = paren_string.split()
    result = []
    for group in groups:
        max_depth = depth = 0
        for char in group:
            if char == '(':
                depth += 1
                max_depth = max(max_depth, depth)
            elif char == ')':
                depth -= 1
        result.append(max_depth)
    return result
