from dataclasses import dataclass

def _getFromKeyOrRaise(key: str, d: dict[str, str]) -> str :
    
    value = d.get(key)

    if(isinstance(value, str)):
        return value
    else:
        raise Exception('Missing value for key: {}'.format(key))

def _getOptionalRatingOrRaise(key: str, d: dict[str, str]) -> int :
    
    rating = d.get(key, 0)

    try:
        return int(rating)
    except:
        raise Exception('Value of key rating is not expected type int, value is: {}'.format(rating))
 
@dataclass
class Book():
    id: str
    title: str
    author: str
    rating: int

    def __init__(self, id: str, title: str, author: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating

    @classmethod
    def fromDict(cls, d: dict[str, str]):
        return cls(
            id= _getFromKeyOrRaise(key='id', d=d),
            title= _getFromKeyOrRaise(key='title', d=d),
            author= _getFromKeyOrRaise(key='author', d=d),
            rating= _getOptionalRatingOrRaise(key='rating', d=d),
            )