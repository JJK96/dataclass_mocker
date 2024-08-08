# Dataclass mocker

Can create an instance of any dataclass by generating arguments based on type annotations.

## Usage

Example:

```
from dataclass_mocker import Mocker
mocker = Mocker()

# Some random class
class MyClass:
    def __init__(self, a: int, b:bool, c:str):
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return "<MyClass " + str(self.__dict__) + ">"

# Instantiate the class
myclass = mocker.instantiate(MyClass)
print(myclass.__dict__)

# Equivalent:
myclass2 = MyClass(**mocker.get_arguments(MyClass))
print(myclass2.__dict__)

# Some random function
def myfunction(a:int, b:bool, c:MyClass):
    return (a, b, c)

# Call the function
print(mocker.call(myfunction))

# Equivalent
print(myfunction(**mocker.get_arguments(myfunction)))
```

If you need to resolve types like the following:

```
def myfunction(a: "MyClass"):
    pass
```

Create a subclass of Mocker and override the `string_to_type` function:

```
class MyMocker(Mocker):
    def string_to_type(self, typestring):
        return globals().get(typestring)

mocker = MyMocker()
```

You can also override any of the `generate_*` functions to change the logic for generating values of that type.
