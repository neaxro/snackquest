from .order import Order
from .snack import Snack

class Node:
    def __init__(self, price: int, balance: int) -> None:
        self.price: int = price
        self.balance: int = balance
        self.childs: list[Node] = []
        self.order: list[int] = []
        
    def add_child(self, price: int):
        child = Node(price, self.balance - price)
        child.order = self.order.copy()
        child.order.append(price)
        
        self.childs.append(child)
        
        return child
    
    def get_order(self, snacks: list[Snack]) -> list[Order]:
        order: list[Order] = []
        
        for snack_price in set(self.order):
            
            # The choosable snack names
            snack_names = []
            for snack in snacks:
                if snack.price == snack_price:
                    snack_names.append(snack.name)
            
            order.append(
                Order(
                    snack_price,
                    self.order.count(snack_price),
                    set(snack_names)
                )
            )
        
        return order
            

def my_dfs(node: Node) -> list[Node]:
    possible_orders: list[Node] = []
    
    for child in node.childs:
        if len(child.childs) == 0:
            possible_orders.append(child)
            return possible_orders
        else:
            result = my_dfs(child)
            possible_orders.extend(result)
            
    return possible_orders

# Build tree recursively
def build_graph(node: Node, prices):
    for price in prices:
        if node.balance - price >= 0:
            child = node.add_child(price)
            build_graph(child, prices)
        else:
            return