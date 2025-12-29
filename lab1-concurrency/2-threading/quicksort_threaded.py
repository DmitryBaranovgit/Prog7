import threading

def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left, middle, right = [], [], []

    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            middle.append(x)
    
    left_sorted = []
    right_sorted = []

    def sort_left():
        nonlocal left_sorted
        left_sorted = quicksort(left)

    def sort_right():
        nonlocal right_sorted
        right_sorted = quicksort(right)
    
    t1 = threading.Thread(target=sort_left)
    t2 = threading.Thread(target=sort_right)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return left_sorted + middle + right_sorted

data = [5, 3, 8, 4, 2, 7, 1, 6]
print(quicksort(data))