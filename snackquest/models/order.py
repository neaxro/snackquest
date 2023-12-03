class Order:
    def __init__(self, price: int, count: int, snacks: list[str]) -> None:
        self.price: int = price
        self.count: int = count
        self.snacks: set[str] = snacks
        
    def show(self) -> None:
        print(f"Price: {self.price} JMF [{self.count}] ({self.snacks})")