from dataclasses import dataclass


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
