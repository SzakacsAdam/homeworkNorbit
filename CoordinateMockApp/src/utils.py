from __future__ import annotations

import asyncio
import ntpath

from typing import Any
from typing import AsyncIterable
from typing import AsyncIterator
from typing import Iterable
from typing import List
from typing import Optional


def get_filename_from_path(path: str) -> str:
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class AIOZipLongest:
    def __init__(self, iterators: List[AsyncIterator]) -> None:
        self.iterators: List[AsyncIterator] = iterators

    def __aiter__(self) -> AIOZipLongest:
        return self

    async def __anext__(self):
        async def collect_next(coro) -> Optional[Any]:
            return await anext(coro, None)

        tasks = (collect_next(task) for task in self.iterators)
        res = await asyncio.gather(*tasks)
        if all(val is None for val in res):
            raise StopAsyncIteration()
        return res


def remove_none_from_list(lst: List) -> List:
    return [
        item
        for item in lst
        if item is not None
    ]


async def sync_to_async_iterator(iterable: Iterable[Any]
                                 ) -> AsyncIterable[Any]:
    for item in iterable:
        yield item
