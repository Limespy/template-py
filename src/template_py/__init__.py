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

    from . import subpackage
else:
    ModuleType = object
# ======================================================================
_SELF: ModuleType = _modules[__package__]
_DYNAMIC_MODULES = ('subpackage', )
# ----------------------------------------------------------------------
def __getattr__(name: str) -> ModuleType:
    if name not in _DYNAMIC_MODULES:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(f'.{name}', __package__)
    setattr(_SELF, name, module)
    return module
