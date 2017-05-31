"""This module provides an reference-cycle proof interface
to the dispatcher.
"""

import weakref

from . import dispatcher
from .dispatcher import DispatchError, Register


__all__ = [
    # errors
    'DispatchError', 
    # classes
    'Register',
    # functions
    'dispatch', 'call',
    'get_var', 'set_var',
    'register', 'register_class',
]


_keep_alive = []
# FIXME: annotate return type weakref.proxy
# How to annotate it returns a proxy to a function
def _proxify(func) -> weakref.ProxyType:
    """Create a weakref.proxy to a function.
    stores a strong reference to keep methods etc.
    alive.

    `func`: Function to be proxied.

    `return`: weakref.proxy to the function.
    """
    _keep_alive.append(func)
    return weakref.proxy(func)

_global_dispatcher = dispatcher.Dispatcher()
dispatch        = _proxify(_global_dispatcher.dispatch)
call            = _proxify(_global_dispatcher.call)
get_var         = _proxify(_global_dispatcher.get_var)
set_var         = _proxify(_global_dispatcher.set_var)
register        = _proxify(_global_dispatcher.register)
register_class  = _proxify(_global_dispatcher.register_class)
