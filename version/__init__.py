import subprocess
from typing import Optional


def version_from_git() -> Optional[str]:
    try:
        return subprocess.check_output(['git', 'describe', '--tag'], universal_newlines=True).rstrip('\n')
    except subprocess.SubprocessError:
        return None


version = version_from_git() or '0.0.0-test'
