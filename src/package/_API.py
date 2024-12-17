import sys
from importlib import import_module
from typing import TYPE_CHECKING

from limedev.CLI import get_main
# ======================================================================
def f() -> None:
    ...
# ======================================================================
main = get_main(__name__)
