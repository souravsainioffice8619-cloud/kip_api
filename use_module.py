from demo_module import add_, multiply_, divide_, subtract_
print("Addition:", add_(10, 5))
print("Multiplication:", multiply_(10, 5))
print("Division:", divide_(10, 5))
print("Subtraction:", subtract_(10, 5))

from new_pakages.demo_module import add_ as add_1, multiply_ as multiply_1, divide_ as divide_1, subtract_ as subtract_1
print("Addition from new_pakages:", add_1(20, 10))
print("Multiplication from new_pakages:", multiply_1(20, 10))
print("Division from new_pakages:", divide_1(20, 10))
print("Subtraction from new_pakages:", subtract_1(20, 10))