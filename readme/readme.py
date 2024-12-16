import pathlib

import package
import yamdog as md
from limedev import readme
#=======================================================================
PATH_BASE = pathlib.Path(__file__).parent
#=======================================================================
def quick_start() -> md.Document:
    example_text = (PATH_BASE / 'examples'/ 'quick_start.py').read_text()

    guide = md.Document([md.Heading('Example', 3),
                         md.CodeBlock(example_text, 'python')])
    return guide
#=======================================================================
def main(pyproject: readme.PyprojectType) -> md.Document:

    name = pyproject['tool']['limedev']['full_name']
    semi_description = md.Document([md.Paragraph([
        f'{name} is'
       '.'
    ])])

    return readme.make(package, semi_description,
                       name = name,
                       abbreviation = 'pkg',
                       quick_start = quick_start())
