# simpale  decorator_ex
def change_case(fun):
    def upper_case():        
        return fun().upper()    
    return upper_case
@change_case
def fun():
    return "hello world"
print(fun())  # Output: HELLO WORLD

# Arguments in the Decorated Function

def decorator_with_param(prefix):
    def upper_case(x):
        return prefix(x).upper()
    return upper_case

@decorator_with_param
def greet(name):
    return f"{name}, welcome!"
print(greet("Alice"))  # Output: GREETING: ALICE, WELCOME!

# *args: Packs positional arguments into a Tuple.
# **kwargs: Packs keyword arguments into a Dictionary.
# Asterisks: The symbols * and ** are the actual logic; "args" and "kwargs" are just names.

# decorator with *args and **kwargs
def decorator_with_args(fun):
    def wrapper(*args, **kwargs):
        print("Arguments passed:", args, kwargs)
        return fun(*args, **kwargs)
    return wrapper
@decorator_with_args
def add(a, b):
    return a + b    
print(add(5, 10))  # Output: Arguments passed: (5, 10) {} 15

# Decorator With Arguments
def decorator_with_argumaent(n = 0):
    def case(fun):
        def warf(*args ,**kwargs):
            if n == 0:
                return fun(*args, **kwargs).lower()
            else:
                return fun(*args, **kwargs).upper()
        return warf
    return case

@decorator_with_argumaent(1)
def fun(msg):  
    return f"Hello World decorator_with_argumaent(1) + {msg}"     
print(fun("Alice , kkkk"))  # Output: HELLO WORLD

# importing fun from first.py
from first import fun
fun("Alice", age=30, city="New York", profession="Engineer")
