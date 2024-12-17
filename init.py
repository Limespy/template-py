import pathlib
import re
import sys
import tomllib
from importlib import import_module
from subprocess import check_output
from types import ModuleType
from typing import Any

from pip._internal.cli.main import main as pip
# ======================================================================
PATH_REPO = pathlib.Path(__file__).parent

_PATTERN_PYVERSION = r"(?<=(py3|\s3\.))"

DEFAULT_PYVERSION_MIN = '11'
DEFAULT_PYVERSION_MAX = '14'

PATTERN_PYVERSION_MIN = re.compile(_PATTERN_PYVERSION + DEFAULT_PYVERSION_MIN)
PATTERN_PYVERSION_MAX = re.compile(_PATTERN_PYVERSION + DEFAULT_PYVERSION_MAX)
PATTERN_DISALLOWED = re.compile(r'[^a-z0-9]')
PATTERN_GH_PYVERSION = re.compile(r"(?<='3.)\d+.(^', )*(?=')")
class Itersub:
    def __init__(self, iterable):
        self.iterable = iter(iterable)
    def __call__(self, _):
        return str(next(self.iterable))
# ======================================================================
def _init_pyproject(tomli_w: ModuleType,
                    full_name: str,
                    pypi_name: str,
                    package_name: str,
                    repo_remote: str,
                    pyversion_min: str,
                    pyversion_max: str,
                    version: str,
                    author: str) -> None:
    path_pyproject = PATH_REPO / 'pyproject.toml'

    with open(path_pyproject, 'r+b') as f:

        pyproject = tomllib.load(f)
        project_config: dict[str, Any] = pyproject['project']

        # Name
        project_config['name'] = pypi_name
        pyproject['tool']['limedev']['full_name'] = full_name

        # Authors
        authors_config: list[dict[str, str]] = project_config['authors']
        author_info = {'name': author}
        if authors_config:
            authors_config[0] = author_info
        else:
            authors_config.append(author_info)

        # Version
        if version:
            project_config['version'] = version

        # Pyversion
        project_config['requires-python'] = '>=3.' + pyversion_min

        # URLs
        url_config: dict[str, str] = project_config['urls']
        url_config['Homepage'] = repo_remote
        url_config['Changelog'] = repo_remote + '/blob/main/README.md#Changelog'
        url_config['Issue Tracker'] = repo_remote + '/issues'

        # Classifiers
        classifiers: list[str] = project_config['classifiers']
        classifiers.sort()
        index_start = classifiers.index("Programming Language :: Python :: 3 :: Only")
        del classifiers[index_start+1:]
        for pyversion in range(int(pyversion_min), int(pyversion_max) + 1):
            classifier = f'Programming Language :: Python :: 3.{pyversion}'
            classifiers.append(classifier)

        # Entry points
        scripts: dict[str, str] = project_config['scripts']
        scripts.pop('template-py', '')
        scripts[pypi_name] = package_name + ':main'

        f.seek(0)
        tomli_w.dump(pyproject, f)
        f.truncate()
# ======================================================================
def init_pyproject(full_name: str,
                   pypi_name: str,
                   package_name: str,
                   repo_remote: str,
                   pyversion_min: str,
                   pyversion_max: str,
                   version: str,
                   author: str) -> None:
    try:
        import tomli_w
        _init_pyproject(tomli_w,
                        full_name,
                        pypi_name,
                        package_name,
                        repo_remote,
                        pyversion_min,
                        pyversion_max,
                        version,
                        author)
    except ModuleNotFoundError:
        try:
            pip(['install', 'tomli-w', '-y'])
            tomli_w = import_module('tomli_w')
            _init_pyproject(tomli_w,
                            full_name,
                            pypi_name,
                            package_name,
                            repo_remote,
                            pyversion_min,
                            pyversion_max,
                            version,
                            author)
        finally:
            pip(['uninstall', 'tomli-w', '-y'])
# ======================================================================
def init_tox_ini(pyversion_min: str, pyversion_max: str) -> None:
    with open(PATH_REPO / 'tox.ini', 'r+') as f:
        text = PATTERN_PYVERSION_MIN.sub(pyversion_min, f.read())
        text = PATTERN_PYVERSION_MAX.sub(pyversion_max, text)

        f.seek(0)
        f.write(text)
        f.truncate()
# ======================================================================
def init_gh_actions_tests(pyversion_min: str, pyversion_max: str) -> None:

    path_workflows = PATH_REPO / '.github' / 'workflows'

    with open(path_workflows / 'tests.yaml', 'r+') as f:
        text = PATTERN_GH_PYVERSION.sub(Itersub((pyversion_min, pyversion_max)),
                                        f.read(), 2)
        f.seek(0)
        f.write(text)
        f.truncate()

    for workflow in ('publish_main', 'publish_candidate'):
        with open(path_workflows / (workflow + '.yaml'), 'r+') as f:
            text = PATTERN_GH_PYVERSION.sub(pyversion_min, f.read())
            f.seek(0)
            f.write(text)
            f.truncate()
# ======================================================================
def init_package(package_name: str) -> None:
    for path in (PATH_REPO / 'src').iterdir():
        if path.is_dir() and (path / '__init__.py').exists():
            path.rename(path.parent / package_name)
# ======================================================================
def main(args: list[str] = sys.argv[1:]):

    full_name = args.pop(0)
    kwargs = {'pyversion': ',',
              'version': ''}
    for arg in args:
        if arg.startswith('--'):
            key, _, value = arg[2:].partition('=')
            kwargs[key] = value

    pyversion_min, _, pyversion_max = kwargs['pyversion'].partition(',')

    if not pyversion_min:
        pyversion_min = DEFAULT_PYVERSION_MIN
    if not pyversion_max:
        pyversion_max = DEFAULT_PYVERSION_MAX

    _repo = check_output(('git', 'remote', '-v')
                        ).split(b'@', 1)[1].split(b'.git', 1)[0]
    author = _repo.split(b':', 1)[1].split(b'/', 1)[0].decode('utf-8')

    repo_remote = 'https://' + _repo.replace(b':', b'/').decode('utf-8')

    pypi_name = PATTERN_DISALLOWED.sub('-', full_name.lower())
    package_name = PATTERN_DISALLOWED.sub('_', pypi_name)

    init_pyproject(full_name = full_name,
                   pypi_name = pypi_name,
                   package_name = package_name,
                   repo_remote = repo_remote,
                   pyversion_min = pyversion_min,
                   pyversion_max = pyversion_max,
                   version = kwargs['version'],
                   author = author)
    init_tox_ini(pyversion_min, pyversion_max)
    init_gh_actions_tests(pyversion_min, pyversion_max)
    init_package(package_name)
# ======================================================================
if __name__ == '__main__':
    raise SystemExit(main())
