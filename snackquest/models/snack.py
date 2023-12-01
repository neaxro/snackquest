class Snack:
    def __init__(self, name, price, desired) -> None:
        self.name: str = name
        self.price: int = price
        self.desired: int = desired
        self.tobuy: int = 0
    
    def __repr__(self) -> str:
        return f"{self.name} (price: {self.price} JMF, desired: {self.desired} db, to buy: {self.tobuy} db)"
