import random
import typing
import string
from enum import EnumType
import inspect

class Mocker:
    def generate_str(self, param, paramtype):
        l = random.randint(0, 20)
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(l))
    
    def generate_int(self, param, paramtype):
        return random.choice([0,1,10,100])

    def generate_bool(self, param, paramtype):
        return random.choice([True, False])

    def generate_list(self, param, paramtype):
        return []

    def generate_dict(self, param, paramtype):
         return {}

    def generate_enum(self, param, paramtype):
        return random.choice(list(paramtype))

    def generate_class(self, param, paramtype):
        return self.instantiate(paramtype)

    def string_to_type(self, typestring):
        raise NotImplemented

    def generate_mock_value(self, param):
        paramtype = param.annotation
        if isinstance(param.annotation, typing._GenericAlias):
            paramtype = param.annotation.__origin__
        elif isinstance(param.annotation, str):
            paramtype = self.string_to_type(param.annotation)
        if paramtype == int:
            return self.generate_int(param, paramtype)
        elif paramtype == str:
            return self.generate_str(param, paramtype)
        elif paramtype == bool:
            return self.generate_bool(param, paramtype)
        elif paramtype == list:
            return self.generate_list(param, paramtype)
        elif paramtype == dict:
            return self.generate_dict(param, paramtype)
        elif isinstance(paramtype, EnumType):
            return self.generate_enum(param, paramtype)
        elif inspect.isclass(paramtype):
            return self.generate_class(param, paramtype)
        else:
            return None

    def get_arguments(self, cls):
        """
        arguments:
            cls: Class or function to generate keyword arguments for based on type
        """
        signature = inspect.signature(cls)
        arguments = {}

        for name, param in signature.parameters.items():
            if param.default == inspect.Parameter.empty and param.annotation != inspect.Parameter.empty:
                arguments[name] = self.generate_mock_value(param)
            elif param.default != inspect.Parameter.empty:
                arguments[name] = param.default
        
        return arguments

    def instantiate(self, cls):
        return cls(**self.get_arguments(cls))

    call = instantiate
