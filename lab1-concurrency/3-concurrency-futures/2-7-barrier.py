import threading

barrier = threading.Barrier(2)

def server():
    print("Server ready")
    barrier.wait()

def client():
    barrier.wait()
    print("Client sends requests")

threading.Thread(target=server).start()
threading.Thread(target=client).start()