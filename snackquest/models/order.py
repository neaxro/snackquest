from models.snack import Snack

class Order:
    def __init__(self, balance: int, snacks: list[Snack]) -> None:
        self.balance: int = balance
        self.snacks: list[Snack] = snacks
        
    def show(self) -> None:
        print(f"Balance: {self.balance} JMF")
        for snack in self.snacks:
            print(f"{snack.name}({snack.price * snack.tobuy} JMF): {snack.tobuy} db")
