
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import List
from typing import Optional

from file_handling import FileFinder
from file_handling import CsvDictReader
from utils import sync_to_async_iterator
from utils import AIOZipLongest


class Collection(ABC):
    def __init__(self, resource_dir: str) -> None:
        self._file_finder: FileFinder = FileFinder(resource_dir)
        self._data: Optional[List[Any]] = None

    @abstractmethod
    def get_iterator(self):
        raise NotImplementedError()

    @abstractmethod
    async def collect(self) -> None:
        raise NotImplementedError()

    @property
    def is_data(self) -> bool:
        if self._data is None:
            return False


class InMemoryCollection(Collection):

    def get_iterator(self):
        return sync_to_async_iterator(self._data)

    async def collect(self) -> None:
        files = [CsvDictReader(file) for file in
                 self._file_finder.get_files_by_extension()]
        self._data: List[str] = [
            row
            async for row in AIOZipLongest(files)
        ]


class ReaderCollection(Collection):

    def get_iterator(self):
        files = [data.new() for data in
                 self._data]
        return AIOZipLongest(files)

    async def collect(self) -> None:
        self._data: List[CsvDictReader] = [
            CsvDictReader(file)
            for file in self._file_finder.get_files_by_extension()
        ]
