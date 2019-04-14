import typing

tk = str
tv = int
td = typing.Dict[tk,tv]

constants : td = {'pi':3.14} # correctly complains Dict entry 0 has incompatible type "str": "float"; expected "str": "int"

def get_type() -> type:
    tk = str
    tv = int
    t = typing.Dict[tk,tv]
    return t

td2 = get_type()

constants2 : td2 = {'pi':3.14} 
