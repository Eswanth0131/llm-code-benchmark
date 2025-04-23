def check_dict_case(dictionary: dict) -> bool:
    if not dictionary:
        return False
    keys = dictionary.keys()
    if all(isinstance(k, str) and k.islower() for k in keys):
        return True
    if all(isinstance(k, str) and k.isupper() for k in keys):
        return True
    return False
