import random
import typing
import string
from enum import EnumType
import inspect
from datetime import date, datetime

class SkipArgument(Exception):
    pass

class Mocker:
    to_override = [None]
    def __init__(self, to_override=None):
        if to_override is not None:
            self.to_override = to_override

    def generate_str(self, param, paramtype):
        l = random.randint(0, 20)
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(l))
    
    def generate_int(self, param, paramtype):
        return random.choice([0,1,10,100])

    def generate_float(self, param, paramtype):
        return random.uniform(0, 1)

    def generate_bool(self, param, paramtype):
        return random.choice([True, False])

    def generate_list(self, param, paramtype):
        return []

    def generate_dict(self, param, paramtype):
         return {}

    def generate_date(self, param, paramtype):
        return date.today()

    def generate_datetime(self, param, paramtype):
        return datetime.today()

    def generate_enum(self, param, paramtype):
        return random.choice(list(paramtype))

    def generate_class(self, param, paramtype):
        return self.instantiate(paramtype)

    def get_union_type(self, param, paramtype):
        return random.choice(paramtype.__args__)

    def string_to_type(self, typestring):
        raise NotImplemented

    def generate_mock_value(self, param, paramtype=None):
        if paramtype is None:
            paramtype = param.annotation
        if paramtype is None:
            return None
        if isinstance(paramtype, typing._UnionGenericAlias):
            paramtype = self.get_union_type(param, paramtype)
            return self.generate_mock_value(param, paramtype)
        elif isinstance(paramtype, typing._GenericAlias):
            paramtype = paramtype.__origin__
            return self.generate_mock_value(param, paramtype)
        elif isinstance(paramtype, typing.ForwardRef):
            paramtype = paramtype.__forward_arg__
            return self.generate_mock_value(param, paramtype)
        elif isinstance(paramtype, str):
            paramtype = self.string_to_type(paramtype)
            return self.generate_mock_value(param, paramtype)
        elif paramtype == int:
            return self.generate_int(param, paramtype)
        elif paramtype == float:
            return self.generate_float(param, paramtype)
        elif paramtype == str:
            return self.generate_str(param, paramtype)
        elif paramtype == bool:
            return self.generate_bool(param, paramtype)
        elif paramtype == list:
            return self.generate_list(param, paramtype)
        elif paramtype == dict:
            return self.generate_dict(param, paramtype)
        elif paramtype == date:
            return self.generate_date(param, paramtype)
        elif paramtype == datetime:
            return self.generate_datetime(param, paramtype)
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
        try:
            signature = inspect.signature(cls)
        except ValueError:
            return {}
        arguments = {}

        for name, param in signature.parameters.items():
            try:
                if (param.default == inspect.Parameter.empty or param.default in self.to_override) \
                        and param.annotation != inspect.Parameter.empty:
                    arguments[name] = self.generate_mock_value(param)
                elif param.default != inspect.Parameter.empty:
                    arguments[name] = param.default
            except SkipArgument:
                continue
        
        return arguments

    def instantiate(self, cls):
        return cls(**self.get_arguments(cls))

    call = instantiate
