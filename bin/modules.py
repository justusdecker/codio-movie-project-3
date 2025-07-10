def compare_two_strings(a: str, b: str) -> int:
    return any([b.count(char) >= a.count(char) and char in b for char in a])

def error(msg: str) -> None:
    """ prints a text in ✨fancy red✨ """
    print(f"\033[0;31m{msg}\033[0m")
    
def convert_to_float(text:str) -> bool | float:
    """
    Return the float: convert is possible
    Return False: Error occured
    """
    if text.count(".") == 0 and text.isdecimal():
        return float(text)
    if text.count(".") == 1 and text != '.':
        a,b = text.split(".")
        if a + b == 2: return False #Is not a float
        return float(f"{a + '.' if a.isdecimal() else '0.'}{b if b.isdecimal() else '0'}")
    return False

def get_user_input_colorized(msg):
    _ret = input(f"{msg}\033[1;32m")
    print("\033[0m",end="")
    return _ret
