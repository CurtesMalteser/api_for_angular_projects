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
    title: str
    author: str

    def __init__(self, id: str, title: str, author: str):
        self.id = id
        self.title = title
        self.author = author

    @classmethod
    def fromDict(cls, d: dict[str, str]):
        return cls(
            id= _getFromKeyOrRaise(key='id', d=d),
            title= _getFromKeyOrRaise(key='title', d=d),
            author= _getFromKeyOrRaise(key='author', d=d),
            )