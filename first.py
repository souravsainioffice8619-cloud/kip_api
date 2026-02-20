def fun(name , **data):
    print("Name:", name)
    for key , value in data.items():
        print(f"{key} : {value}")
    # print("this output is using .get() method",data.get("age"))
    print("this output is using .get() method",data.get("profession"))
    print("this output is using .get() method",data.get("city"))
# egh

# **data is used to pass a variable number of keyword arguments to a function.
# **data collects these keyword arguments into a dictionary named 'data'.

class demo:
    baseinfo = {"name":"Alice" , "age":30 , "country":"Wonderland"}
    def __init__(self , **info):
        self.info = info

    def show_info(self):
        for key , value in self.info.items():
            print(f"{key} : {value}")
    
    @classmethod
    def clm(cls, **info):
        return cls(info=info)
    
    @classmethod
    def setdata(cls , **data):
        cls.baseinfo = data
    
    @classmethod
    def getdata(cls):
        return cls.baseinfo
    
    @staticmethod
    def thisstatic(): # static method does not take self or cls as first parameter
        print("This is a static method.")
    
    def retself(self):
        return self

if __name__ == "__main__":
    fun("Alice", age=30, city="New York", profession="Engineer")
    obj = demo(name="Bob" , age=25 , country="USA")
    obj.show_info()
    print("Returned info:", obj.retself())
    obj1  = demo.clm(name="Charlie" , age=28 , country="Canada")
    # obj2 = demo(**demo.info)
    # obj2.show_info() #obj is used to unpack the dictionary 'data' into keyword arguments when calling a function.
    print("Base Info before setting new data:", demo.getdata())
    demo.setdata(name="Diana" , age=32 , country="UK")
    print("Base Info after setting new data:", demo.getdata())