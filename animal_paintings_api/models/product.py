from dataclasses import dataclass

@dataclass
class Product():
    id: int
    name: str
    price: float
    image_url: str

    def __init__(self, id: int, name: str, price: float,image_url: str):
        self.id = id
        self.name = name
        self.price = price
        self.image_url =   image_url

    @classmethod
    def fromDict(cls, d: dict[any, any]):
        return cls(
            id= str(d.get('id')),
            name= str(d.get('name')),
            price= str(d.get('price')),
            image_url= str(d.get('image_url')),
            )
