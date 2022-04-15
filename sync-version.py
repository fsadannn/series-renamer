import sys
from pathlib import Path

import tomli

with open("pyproject.toml", "rb") as f:
    toml_dict = tomli.load(f)

version = toml_dict['tool']['poetry']['version']


script_dir = Path(__file__).parent

sys.path.insert(0, str(script_dir))

import series_renamer

sys.path.pop(0)

if series_renamer.__version__ != version:
    with open(script_dir.joinpath('series_renamer', 'version.py'), 'w') as f:
        f.write(f'ersion = "{version}"')
