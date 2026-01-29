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