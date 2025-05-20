# type: ignore
from typing import Optional

_DUMMY_VERSION = '0.0.0.dev0'


def version_from_package() -> Optional[str]:
    try:
        from ._version import version
        return version
    except ImportError:
        return None


version = version_from_package() or _DUMMY_VERSION
