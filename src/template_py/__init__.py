"""Documentation."""
__version__ = '0.0.1'
from importlib import import_module
from typing import TYPE_CHECKING
from sys import modules as _modules

from ._API import *
# ======================================================================
# Hinting types
if TYPE_CHECKING:
    from types import ModuleType

    from . import debug
else:
    ModuleType = object
# ======================================================================
def __getattr__(name: str) -> ModuleType:
    if name not in ('debug', ):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(f'.{name}', __package__)
    setattr(_modules[__package__], name, module)
    return module
