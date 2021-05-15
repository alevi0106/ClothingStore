import enum

class CategoryTypeEnum(enum.Enum):
    SIZE = 1
    GENDER = 2
    TAG = 3
    COLOR = 4

class SizeEnum(enum.Enum):
    S = 1
    M = 2
    L = 3
    XL = 4
    XXL = 5

class GenderEnum(enum.Enum):
    Male = 1
    Female = 2

class TagEnum(enum.Enum):
    TShirt = 1
    Pants = 2
    Suit = 3
    Saree = 4
    Jeans = 5
    PunjabiDress = 6
    Chino=7

class ColorEnum(enum.Enum):
    Red = 1
    Blue = 3
    Black = 3
    White = 4
    Pink = 5
    Grey = 6
    Green = 7
    Yellow = 8
    Violet = 9
    Indigo = 10
