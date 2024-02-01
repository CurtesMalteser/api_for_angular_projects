from dataclasses import dataclass

def _getFromKeyOrRaise(key: str, d: dict[str, str]) -> str :
    
    value = d.get(key)

    if(isinstance(value, str)):
        return value
    else:
        raise Exception('Missing value for key: {}'.format(key))

@dataclass
class Book():
    id: str
    name: str
    author: str

    def __init__(self, id: str, name: str, author: str):
        self.id = id
        self.name = name
        self.author = author

    @classmethod
    def fromDict(cls, d: dict[str, str]):
        return cls(
            id= _getFromKeyOrRaise(key='id', d=d),
            name= _getFromKeyOrRaise(key='name', d=d),
            author= _getFromKeyOrRaise(key='author', d=d),
            )