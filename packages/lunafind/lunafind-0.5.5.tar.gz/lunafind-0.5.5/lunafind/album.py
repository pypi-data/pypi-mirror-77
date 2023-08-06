# Copyright 2018 miruka
# This file is part of lunafind, licensed under LGPLv3.

import traceback
from typing import Generator, List

from . import LOG, order
from .attridict import AttrIndexedDict
from .filtering import filter_all
from .post import Post
from .stream import Stream


class Album(AttrIndexedDict, attr="id", map_partials=("download",)):
    def __init__(self, *stream_args_posts_streams, **stream_kwargs) -> None:
        super().__init__()
        self._added: int = 0
        self.put(*stream_args_posts_streams, **stream_kwargs)


    def __repr__(self) -> str:
        return "%s({\n%s\n})" % (
            type(self).__name__,
            "\n".join((f"  {i!r}: '{p.title:.64}'," for i, p in self.items()))
        )


    @property
    def list(self) -> List[Post]:
        return list(self.values())


    def _put_post(self, post: Post) -> None:
        try:
            super().put(post)
            self._added += 1
        except StopIteration:
            raise
        except Exception:
            traceback.print_exc()
            LOG.error("Unexpected error while handling post %d, "
                      "trying to recover...", post.id)

    def _put_stream(self, stream: Stream) -> None:
        for post in stream:
            self._put_post(post)

    # pylint: disable=arguments-differ
    def put(self, *stream_args_posts_streams, **stream_kwargs) -> "Album":
        stream_args = []
        self._added = 0

        try:
            for arg in stream_args_posts_streams:
                if isinstance(arg, Post):
                    self._put_post(arg)

                elif isinstance(arg, Stream):
                    self._put_stream(arg)

                else:
                    stream_args.append(arg)

            if stream_args or stream_kwargs:
                self._put_stream(Stream(*stream_args, **stream_kwargs))

        except KeyboardInterrupt:
            LOG.warning("Caught CTRL-C, added %d posts.", self._added)

        return self


    def filter(self, search: str, partial_tags: bool = False) -> "Album":
        return Album(*self.filter_lazy(search, partial_tags))

    def filter_lazy(self, search: str, partial_tags: bool = False
                   ) -> Generator[Post, None, None]:
        yield from filter_all(self.list, search, partial_tags=partial_tags)

    def order(self, by: str) -> "Album":
        return Album(*order.sort(self.list, by))

    __truediv__  = lambda self, search: self.filter(search)        # /
    __floordiv__ = lambda self, search: self.filter(search, True)  # //
    __mod__      = lambda self, by:     self.order(by)             # %
