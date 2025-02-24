from typing import TYPE_CHECKING
# ======================================================================
# Hinting types
if TYPE_CHECKING:
    ...
else:
    ...
# ======================================================================

# ======================================================================
def main():
    import sys
    if '--version' in sys.argv:
        print('Template Py', sys.modules[__package__].__version__)
