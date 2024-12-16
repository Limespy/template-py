import package
from limedev.test import BenchmarkResultsType
from limedev.test import eng_round
from limedev.test import run_timed
# ======================================================================
def main() -> tuple[str, BenchmarkResultsType]:
    return package.__version__, {}
