class MyClass:
    class_id = 0

    def __init__(self, my_id):
        self.my_id = my_id
    
    def __repr__(self):
        return f"{type(self).__name__}({self.my_id})"
    
    def method(self):
        print(F"Called method on {self}")
        
    @classmethod
    def construct(cls):
        result = cls(cls.class_id)
        cls.class_id += 1
        return result

class YourClass(MyClass):
    class_id = 0

def main():
    print(f"Building MyClass instance:   {MyClass.construct()}")
    print(f"Building MyClass instance:   {MyClass.construct()}")
    print(f"Building YourClass instance: {YourClass.construct()}")
    print(f"Building YourClass instance: {YourClass.construct()}")
    print(f"Building MyClass instance:   {MyClass.construct()}")
    print(f"Building MyClass instance:   {MyClass.construct()}")
    print(f"Building YourClass instance: {YourClass.construct()}")
    print(f"Building YourClass instance: {YourClass.construct()}")

if __name__ == "__main__":
    main()
