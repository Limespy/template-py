import sys
from importlib import import_module
from typing import TYPE_CHECKING

from limedev.CLI import get_main
# ======================================================================
# Hinting types
if TYPE_CHECKING:
    from types import ModuleType
    from typing import Any
else:
    ModuleType = Any = object
# ======================================================================
_SELF: dict[str, Any] = sys.modules[__package__].__dict__
# ======================================================================
def __getattr__(name: str) -> ModuleType:
    if name not in ('subpackage', ):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(f'.{name}', __package__)
    _SELF[name] = module
    return module
# ======================================================================
def f() -> None:
    ...
# ======================================================================
main = get_main(__name__)
