from typing import Iterable


class Memory(list):
    def __init__(self, iterable: Iterable[int]):
        super().__init__(item for item in iterable)

    def __setitem__(self, index: int, item: int):
        self._ensure_valid(index)

        super().__setitem__(index, item)

    def __getitem__(self, index: int | slice) -> int:
        if isinstance(index, slice):
            """
            This does not guarantee that accessing a new index would return 0.
            But handling that was too much of a performance hit. Unless I really
            need it, I will keep this as is.
            """
            return super().__getitem__(index)
        else:
            self._ensure_valid(index)

            return super().__getitem__(index)

    def _ensure_valid_index(self, index: int):
        if index < 0:
            raise IndexError("Negative index not supported")

    def _ensure_capacity(self, index: int):
        length = super().__len__()
        if length > index:
            return

        self.extend([0 for _ in range(length, index + 1)])

    def _ensure_valid(self, index: int):
        self._ensure_valid_index(index)
        self._ensure_capacity(index)
