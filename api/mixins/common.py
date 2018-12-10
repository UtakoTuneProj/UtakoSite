import json

def isvalid_range(txt):
    if txt is None:
        return False
    pos = json.loads(txt)
    if type(pos) not in (list, tuple):
        return False
    if len(pos) != 8:
        return False
    return True
