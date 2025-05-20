# type: ignore
from typing import Optional

_DUMMY_VERSION = '0.0.0.dev0'


def version_from_pyproject() -> Optional[str]:
    try:
        import tomli
        from pathlib import Path
        path = Path(__file__).parent.parent / "pyproject.toml"
        with path.open("rb") as f:
            pyproject = tomli.load(f)
        return pyproject["project"]["version"]
    except ImportError:
        return None


version = version_from_pyproject() or _DUMMY_VERSION
