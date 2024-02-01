from dataclasses import dataclass

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
            id= str(d.get('id')),
            name= str(d.get('name')),
            author= str(d.get('author')),
            )
