import enum
import types
import typing
import weakref


class DispatchError(RuntimeError):
    """Exception raised when an exception is raised
    during the execution of a registerd function
    in the dispatcher.
    """


class Register(enum.IntFlag):
    """Enum to select registering mode for
    Dispatcher.register_class.
    """
    cls = enum.auto()
    methods = enum.auto()
    staticmethods = enum.auto()
    classmethods = enum.auto()
    classvariables = enum.auto()


class Dispatcher(object):
    """Dynamic dispatcher to glue together all modules
    of the app into one place for easy use across modules.
    """

    def __init__(self):
        self.functions = {}
        self.variables = {}

    def dispatch(self, func_name: str, *args, **kwargs) -> typing.Any:
        """Call and return the result of a
        function previously registered.

        `func_name`: Name of the function.
        `*args`: Positional arguments to be passed to the function.
        `**kwargs`: Keyword-arguments to be passed to the function.

        `return`: Value returned by the function.

        - Raise AttributeError when function is not found.
        - Raise DispatchError when an error occurred whilst
            executing the function. the __cause__ will be set
            to the original exceptio.
        """
        try:
            func = self.functions[func_name]
        except KeyError:
            raise AttributeError(f'No such function {func_name!r}') from None
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            # Catching a bare 'Exception' shouldn't be done in general.
            # However, it's immediately re-raised, so it shouldn't
            # be too big of a deal :)
            raise DispatchError('Exception during function dispatch') from exc

    def call(self, func_name: str, *args, **kwargs) -> typing.Any:
        """Call and return the result of a
        function previously registered.

        `func_name`: Name of the function.
        `*args`: Positional arguments to be passed to the function.
        `**kwargs`: Keyword-arguments to be passed to the function.

        `return`: Value returned by the function.

        - Raise AttributeError when function is not found.
        - Raise DispatchError when an error occurred whilst
            executing the function. the __cause__ will be set
            to the original exceptio.
        """
        return self.dispatch(func_name, *args, **kwargs)

    # call is currently equivalent to dispatch.
    # This implies docstring equivalency.
    # Putting this assert here to ensure that I do not
    # update one but forget the other.
    # NOTE: This may change slightly in the future.
    assert call.__doc__ == dispatch.__doc__, 'Docstring inconsistency'


    # TODO/FIXME: How do we annotate that this function returns
    # a weakref.proxy?
    # How would one go about annotating a function returning
    # a weakref.proxy which is a proxy for a specific type
    # such as a list or dictionary?
    # It cannot be done directly using the types from the
    # weakref module,
    # and there exists no support for this in the typing
    # module.
    #
    # Relevant sources:
    # https://github.com/python/mypy/issues/3142
    def get_var(self, name: str) -> typing.Any:
        """Return a variable previously registerd
        using the set_var function.

        `name`: Name of the variable.

        `return`: A weakref.proxy to the object the name is referring to.

        - Raise AttributeError when no variable with given name exists.
        """
        try:
            # Is a weakref.proxy really necessary?
            return weakref.proxy(self.variables[name])
        except KeyError:
            raise AttributeError(f'No such variable {name!r}') from None

    def set_var(self, name: str, value: typing.Any):
        """Set the value of a global variable.
        It can later be retrieved using the get_var function.

        `name`: Name of the variable.
        `value`: Value the name should refer to.
        """
        # Do not place a weakref here;
        # values are meant to be stored in the dispatcher
        # and not in a module as a regular global variable.
        self.variables[name] = value

    # Avoid too long lines
    _t = typing.Union[types.FunctionType, type, None]
    _r = typing.Union[None, types.FunctionType]

    def register(self, obj: _t=None, **kwargs) -> _r:
        """Register a function, so that it can be called by
        the dispatcher.

        `obj`: Either a function or a class.
                It will be registered with its __name__ as name.
                It is returned after registering; That makes
                this function usable as a decorator.
        `**kwargs`: If `obj` is not given, one can pass 1
                keyword argument in order to register
                a class or function with a specific name.

        `return`: Function or class passed in if it was
                    passed as `obj`.

        - Raise ValueError when both `obj` and `kwargs` are given.
        - Raise ValueError when more than 1 keyword argument is given.
        - Raise ValueError when neither of `obj` or `kwargs` is given.
        """
        if obj is not None and kwargs:
            msg = ('Passing in both an positional and'
                   ' a keyword argument is not allowed')
            raise ValueError(msg)
        elif obj is not None:
            self.__register(**{obj.__name__: obj})
            return obj
        elif kwargs:
            if len(kwargs) > 1:
                msg = (f'Only one keyword argument allowed '
                       f'(got {len(kwargs)}')
                raise ValueError(msg)
            name, attr = next(iter(kwargs.items()))
            # WEAKREF PROXY LOCATION
            self.functions[name] = weakref.proxy(attr)
        else:
            msg = f'{type(self).__name__}.register needs an argument'
            raise ValueError(msg)

    __register = register   # Avoid bugs with overwriting subclass.
    del _t, _r              # Avoid namespace pollution

    def register_class(self, cls: type, register_flags: Register) -> type:
        """Register a class and its components.

        `cls`: The class which (components) should be registered.
        `register_flags`: Bitflag to indicate what parts of the
                class should be registerd. Should be an instance of the
                'Register' enum.

        `return`: Returns the class in order for this function to
                to be used as a decorator.
        """
        if register_flags & Register.cls:
            self.__register(cls)
        for name, attr in vars(cls).items():
            if isinstance(attr, staticmethod):
                if register_flags & Register.staticmethods:
                    self.__register(attr)
            elif isinstance(attr, classmethod):
                if register_flags & Register.classmethods:
                    self.__register(attr)
            elif callable(attr):
                if register_flags & Register.methods:
                    self.__register(attr)
            elif register_flags & Register.variables:
                self.set_var(name, attr)
        return cls
