import tomllib
from pathlib import Path
from typing import Any


def _get_pyproject() -> dict[str, Any]:
    pyproject_path = Path(__file__).parents[2].resolve() / "pyproject.toml"
    try:
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
        return data
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        raise RuntimeError(f"Failed to load pyproject.toml from {pyproject_path}")


__pyproject = _get_pyproject()

__version__ = __pyproject["project"].get("version", "0.0.0")
__description__ = __pyproject["project"].get("description", "")
