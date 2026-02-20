# Threading in Python
# Python provides the threading module to work with threads.

# Steps to Create and Run Threads
# 1: Import the module

# import threading

# 2: Create threads

# t1 = threading.Thread(target=func1, args=(...,))
# t2 = threading.Thread(target=func2, args=(...,))

# 3: Start threads

# t1.start()
# t2.start()

# 4: Wait for completion

# t1.join()
# t2.join()

import threading
import time
def print_numbers():
    for i in range(1, 6):
        print(f"Number: {i}")
        time.sleep(1)
def print_letters():
    for letter in ['A', 'B', 'C', 'D', 'E']:
        print(f"Letter: {letter}")
        time.sleep(1)
# Create threads
t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)
# Start threads
t1.start()
t2.start()
# Wait for completion
t1.join()
t2.join()
print("Finished executing threads.")
# Output may vary in order due to concurrent execution
def fun(name , **data):
    print("Name:", name)
    for key , value in data.items():
        print(f"{key} : {value}")
    # print("this output is using .get() method",data.get("age"))
    print("this output is using .get() method",data.get("profession"))
    print("this output is using .get() method",data.get("city"))

fun("Alice", age=30, city="New York", profession="Engineer")
# egh
# **data is used to pass a variable number of keyword arguments to a function.
# **data collects these keyword arguments into a dictionary named 'data'.
