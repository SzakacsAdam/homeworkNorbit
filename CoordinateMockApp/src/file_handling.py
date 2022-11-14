from os import walk as os_walk
from os.path import join as path_join
from typing import Generator


class FileFinder:
    _DEFAULT_EXT: str = ".csv"
    __slots__ = ("_src",)

    def __init__(self, src: str) -> None:
        self._src: str = src

    def get_all_files(self) -> Generator[str, None, None]:
        for root, _, files in os_walk(self._src, topdown=False):
            for file in files:
                yield path_join(root, file)

    def get_files_by_extension(self, ext: str = _DEFAULT_EXT
                               ) -> Generator[str, None, None]:
        for file in self.get_all_files():
            if file.endswith(ext):
                yield file


class CsvDictReader:
    ...


class CoordinateCollection:
    ...
