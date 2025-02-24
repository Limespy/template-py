"""Documentation."""
from typing import TYPE_CHECKING

from ._API import *
# ======================================================================
# Hinting types
if TYPE_CHECKING:
    from types import ModuleType as _ModuleType

    from . import subpackage
else:
    _ModuleType = object
# ======================================================================
def __getattr__(name: str) -> _ModuleType | str:
    if name in {'subpackage', }:
        from importlib import import_module
        from sys import modules as _modules

        module = import_module(f'.{name}', __package__)

        setattr(_modules[__package__], name, module)
        return module
    elif name == '__version__':
        from importlib import metadata
        return metadata.version(__package__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
