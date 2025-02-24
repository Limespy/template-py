import pytest
import template_py
# ======================================================================
parametrize = pytest.mark.parametrize
# ======================================================================
class Test__init__:
    # ------------------------------------------------------------------
    def test_subpackage_access(self):
        template_py.subpackage
    # ------------------------------------------------------------------
    def test_version_access(self):
        template_py.__version__
    # ------------------------------------------------------------------
    def test_cli_version(self):
        from subprocess import check_output
        out = check_output(('template_py', '--version'))
        assert out
