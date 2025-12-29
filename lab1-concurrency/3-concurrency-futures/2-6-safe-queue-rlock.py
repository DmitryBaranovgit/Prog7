import threading

class SafeQueue:
    def __init__(self):
        self.data = []
        self.lock = threading.RLock()
    
    def push(self, item):
        with self.lock:
            self.data.append(item)
            
    def pop(self):
        with self.lock:
            return self.data.pop(0)