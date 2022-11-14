from __future__ import annotations

from os import walk as os_walk
from os.path import join as path_join
from typing import Any
from typing import AsyncGenerator
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Optional

import aiofiles
from aiocsv import AsyncDictReader


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
    _DEFAULT_DELIMITER: str = ','
    __slots__ = ("_src", "_delimiter" "_file")

    def __init__(self, src: str, *,
                 delimiter: str = _DEFAULT_DELIMITER) -> None:
        self._src: str = src
        self._delimiter: str = delimiter

        self._file: Optional[
            AsyncGenerator[Dict, None, None]] = self.csv_reader()

    async def csv_reader(self) -> AsyncGenerator[Dict[str, Any], None, None]:
        async with aiofiles.open(self._src) as afp:
            async for row in AsyncDictReader(afp,
                                             delimiter=self._delimiter
                                             ):
                yield row


class CoordinateCollection:
    ...
