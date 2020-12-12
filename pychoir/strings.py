from pychoir import Matcher


class StartsWith(Matcher):
    def __init__(self, start: str):
        super().__init__()
        self.start = start

    def _matches(self, other: str) -> bool:
        return other.startswith(self.start)

    def _description(self) -> str:
        return repr(self.start)


class EndsWith(Matcher):
    def __init__(self, end: str):
        super().__init__()
        self.end = end

    def _matches(self, other: str) -> bool:
        return other.endswith(self.end)

    def _description(self) -> str:
        return repr(self.end)
