class Order:
    def __init__(self, price: int, count: int, snacks: list[str]) -> None:
        self.price: int = price
        self.count: int = count
        self.snacks: set[str] = snacks
        
    def show(self) -> None:
        print(f"Price: {self.price} JMF [{self.count}] ({self.snacks})")
    
    def get_snacks(self) -> str:
        snacks_string = ""
        snacks = list(self.snacks)
        
        for i in range(len(self.snacks) - 1):
            snacks_string += snacks[i] + ", "
        snacks_string += str(snacks[-1])
        
        return snacks_string
        
class Orders:
    def __init__(self, balance: int, orders: list[Order]) -> None:
        self.balance = balance
        self.orders = orders
    
    def show(self) -> None:
        print()
        for order in self.orders:
            order.show()
        print("-----------------")
        print(f"Final balance: {self.balance} JMF")