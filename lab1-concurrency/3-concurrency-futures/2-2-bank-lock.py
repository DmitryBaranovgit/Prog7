import threading
class BankAccount:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()
    
    def deposit(self, amount):
        with self.lock:
            self.balance += amount
    
    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount