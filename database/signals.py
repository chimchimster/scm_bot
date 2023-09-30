from enum import Enum


class Signal(Enum):

    USER_EXISTS = 1
    USER_DOES_NOT_EXIST = 2
    USER_DOES_NOT_AUTHORIZED = 3
    ITEM_EXISTS = 4
    ITEM_DOES_NOT_EXIST = 5

