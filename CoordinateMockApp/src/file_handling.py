from __future__ import annotations

from os import walk as os_walk
from os.path import join as path_join
from typing import Any
from typing import AsyncGenerator
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Optional
from typing import Union

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
    _KEY_FORMAT: Callable = str
    _VAL_FORMAT: Callable = float
    __slots__ = (
        "_src", "_delimiter", "_is_format", "_key_format", "_val_format",
        "_file"
    )

    def __init__(self, src: str, *,
                 delimiter: str = _DEFAULT_DELIMITER,
                 is_format: bool = True,
                 key_format: Callable = _KEY_FORMAT,
                 val_format: Callable = _VAL_FORMAT) -> None:
        self._src: str = src
        self._delimiter: str = delimiter
        self._is_format: bool = is_format
        self._key_format: Callable = key_format
        self._val_format: Callable = val_format

        self._file: Optional[AsyncGenerator[Dict, None, None]] = None

    def __aiter__(self) -> CsvDictReader:
        return self

    async def __anext__(self) -> Union[Dict[str, Any],
                                       Dict[_KEY_FORMAT, _VAL_FORMAT]]:

        if self._file is None:
            self._file = self.csv_reader()

        row = await anext(self._file)

        if self._is_format is True:
            return self.format_dict(row)
        return row

    async def csv_reader(self) -> AsyncGenerator[Dict[str, Any], None, None]:
        async with aiofiles.open(self._src) as afp:
            async for row in AsyncDictReader(afp,
                                             delimiter=self._delimiter
                                             ):
                yield row

    def format_dict(self, data: Dict[str, str]
                    ) -> Dict[_KEY_FORMAT, _VAL_FORMAT]:
        return {
            self._key_format(key): self._val_format(val)
            for key, val in data.items()
        }

    def new(self) -> CsvDictReader:
        return CsvDictReader(
            src=self._src,
            delimiter=self._delimiter,
            is_format=self._is_format,
            key_format=self._key_format,
            val_format=self._val_format
        )
