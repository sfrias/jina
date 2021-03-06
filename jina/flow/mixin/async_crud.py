import warnings
from typing import Union, Iterable, TextIO, Dict

import numpy as np

from ...clients.base import InputFnType, CallbackFnType
from ...enums import DataInputType
from ...helper import deprecated_alias


class AsyncCRUDFlowMixin:
    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def train(self, input_fn: InputFnType,
                    on_done: CallbackFnType = None,
                    on_error: CallbackFnType = None,
                    on_always: CallbackFnType = None,
                    **kwargs):
        """Do training on the current flow

        :param input_fn: An iterator of bytes. If not given, then you have to specify it in **kwargs**.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        warnings.warn(f'{self.train} is under heavy refactoring', FutureWarning)
        async for r in self._get_client(**kwargs).train(input_fn, on_done, on_error, on_always, **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def index_ndarray(self,
                            array: 'np.ndarray',
                            axis: int = 0,
                            size: int = None,
                            shuffle: bool = False,
                            on_done: CallbackFnType = None,
                            on_error: CallbackFnType = None,
                            on_always: CallbackFnType = None,
                            **kwargs):
        """Using numpy ndarray as the index source for the current flow

        :param array: the numpy ndarray data source
        :param axis: iterate over that axis
        :param size: the maximum number of the sub arrays
        :param shuffle: shuffle the the numpy data source beforehand
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_ndarray
        async for r in self._get_client(**kwargs).index(_input_ndarray(array, axis, size, shuffle),
                                                        on_done, on_error, on_always, data_type=DataInputType.CONTENT,
                                                        **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def search_ndarray(self,
                             array: 'np.ndarray',
                             axis: int = 0,
                             size: int = None,
                             shuffle: bool = False,
                             on_done: CallbackFnType = None,
                             on_error: CallbackFnType = None,
                             on_always: CallbackFnType = None,
                             **kwargs):
        """Use a numpy ndarray as the query source for searching on the current flow

        :param array: the numpy ndarray data source
        :param axis: iterate over that axis
        :param size: the maximum number of the sub arrays
        :param shuffle: shuffle the the numpy data source beforehand
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_ndarray
        async for r in self._get_client(**kwargs).search(_input_ndarray(array, axis, size, shuffle),
                                                         on_done, on_error, on_always, data_type=DataInputType.CONTENT,
                                                         **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def index_lines(self,
                          lines: Union[Iterable[str], TextIO] = None,
                          filepath: str = None,
                          size: int = None,
                          sampling_rate: float = None,
                          read_mode: str = 'r',
                          line_format: str = 'json',
                          field_resolver: Dict[str, str] = None,
                          on_done: CallbackFnType = None,
                          on_error: CallbackFnType = None,
                          on_always: CallbackFnType = None,
                          **kwargs):
        """ Use a list of lines as the index source for indexing on the current flow

        :param lines: a list of strings, each is considered as d document
        :param filepath: a text file that each line contains a document
        :param size: the maximum number of the documents
        :param sampling_rate: the sampling rate between [0, 1]
        :param read_mode: specifies the mode in which the file
                is opened. 'r' for reading in text mode, 'rb' for reading in binary
        :param line_format: the format of each line: ``json`` or ``csv``
        :param field_resolver: a map from field names defined in ``document`` (JSON, dict) to the field
            names defined in Protobuf. This is only used when the given ``document`` is
            a JSON string or a Python dict.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_lines
        async for r in self._get_client(**kwargs).index(
                _input_lines(lines, filepath,
                             size=size,
                             sampling_rate=sampling_rate,
                             read_mode=read_mode,
                             line_format=line_format,
                             field_resolver=field_resolver),
                on_done, on_error, on_always, data_type=DataInputType.AUTO,
                **kwargs):
            yield r

    async def index_csv(self,
                        lines: Union[Iterable[str], TextIO],
                        field_resolver: Dict[str, str] = None,
                        size: int = None,
                        sampling_rate: float = None,
                        on_done: CallbackFnType = None,
                        on_error: CallbackFnType = None,
                        on_always: CallbackFnType = None,
                        **kwargs):
        """ Use a list of lines as the index source for indexing on the current flow
        :param lines: a list of strings, each is considered as d document
        :param size: the maximum number of the documents
        :param sampling_rate: the sampling rate between [0, 1]
        :param field_resolver: a map from field names defined in ``document`` (JSON, dict) to the field
            names defined in Protobuf. This is only used when the given ``document`` is
            a JSON string or a Python dict.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_csv
        async for r in self._get_client(**kwargs).index(
                _input_csv(lines,
                           size=size,
                           sampling_rate=sampling_rate,
                           field_resolver=field_resolver),
                on_done, on_error, on_always, data_type=DataInputType.AUTO, **kwargs):
            yield r

    async def index_ndjson(self,
                           lines: Union[Iterable[str], TextIO],
                           field_resolver: Dict[str, str] = None,
                           size: int = None,
                           sampling_rate: float = None,
                           on_done: CallbackFnType = None,
                           on_error: CallbackFnType = None,
                           on_always: CallbackFnType = None,
                           **kwargs):
        """ Use a list of lines as the index source for indexing on the current flow
        :param lines: a list of strings, each is considered as d document
        :param size: the maximum number of the documents
        :param sampling_rate: the sampling rate between [0, 1]
        :param field_resolver: a map from field names defined in ``document`` (JSON, dict) to the field
            names defined in Protobuf. This is only used when the given ``document`` is
            a JSON string or a Python dict.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_ndjson
        async for r in self._get_client(**kwargs).index(
                _input_ndjson(lines,
                              size=size,
                              sampling_rate=sampling_rate,
                              field_resolver=field_resolver),
                on_done, on_error, on_always, data_type=DataInputType.AUTO, **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def index_files(self, patterns: Union[str, Iterable[str]], recursive: bool = True,
                          size: int = None, sampling_rate: float = None, read_mode: str = None,
                          on_done: CallbackFnType = None,
                          on_error: CallbackFnType = None,
                          on_always: CallbackFnType = None,
                          **kwargs):
        """ Use a set of files as the index source for indexing on the current flow

        :param patterns: The pattern may contain simple shell-style wildcards, e.g. '\*.py', '[\*.zip, \*.gz]'
        :param recursive: If recursive is true, the pattern '**' will match any files and
                    zero or more directories and subdirectories.
        :param size: the maximum number of the files
        :param sampling_rate: the sampling rate between [0, 1]
        :param read_mode: specifies the mode in which the file
                is opened. 'r' for reading in text mode, 'rb' for reading in binary mode
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_files
        async for r in self._get_client(**kwargs).index(
                _input_files(patterns, recursive, size, sampling_rate, read_mode),
                on_done, on_error, on_always, data_type=DataInputType.CONTENT,
                **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def search_files(self,
                           patterns: Union[str, Iterable[str]],
                           recursive: bool = True,
                           size: int = None, sampling_rate: float = None, read_mode: str = None,
                           on_done: CallbackFnType = None,
                           on_error: CallbackFnType = None,
                           on_always: CallbackFnType = None,
                           **kwargs):
        """ Use a set of files as the query source for searching on the current flow

        :param patterns: The pattern may contain simple shell-style wildcards, e.g. '\*.py', '[\*.zip, \*.gz]'
        :param recursive: If recursive is true, the pattern '**' will match any files and
                    zero or more directories and subdirectories.
        :param size: the maximum number of the files
        :param sampling_rate: the sampling rate between [0, 1]
        :param read_mode: specifies the mode in which the file
                is opened. 'r' for reading in text mode, 'rb' for reading in
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_files
        async for r in self._get_client(**kwargs).search(
                _input_files(patterns, recursive, size, sampling_rate, read_mode),
                on_done, on_error, on_always, data_type=DataInputType.CONTENT, **kwargs):
            yield r

    async def search_ndjson(self,
                            lines: Union[Iterable[str], TextIO],
                            field_resolver: Dict[str, str] = None,
                            size: int = None,
                            sampling_rate: float = None,
                            on_done: CallbackFnType = None,
                            on_error: CallbackFnType = None,
                            on_always: CallbackFnType = None,
                            **kwargs):
        """ Use a list of files as the query source for searching on the current flow
        :param lines: a list of strings, each is considered as d document
        :param size: the maximum number of the documents
        :param sampling_rate: the sampling rate between [0, 1]
        :param field_resolver: a map from field names defined in ``document`` (JSON, dict) to the field
            names defined in Protobuf. This is only used when the given ``document`` is
            a JSON string or a Python dict.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_ndjson
        async for r in self._get_client(**kwargs).search(
                _input_ndjson(lines,
                              size=size,
                              sampling_rate=sampling_rate,
                              field_resolver=field_resolver),
                on_done, on_error, on_always, data_type=DataInputType.AUTO, **kwargs):
            yield r

    async def search_csv(self,
                         lines: Union[Iterable[str], TextIO],
                         field_resolver: Dict[str, str] = None,
                         size: int = None,
                         sampling_rate: float = None,
                         on_done: CallbackFnType = None,
                         on_error: CallbackFnType = None,
                         on_always: CallbackFnType = None,
                         **kwargs):
        """ Use a list of lines as the index source for indexing on the current flow
        :param lines: a list of strings, each is considered as d document
        :param size: the maximum number of the documents
        :param sampling_rate: the sampling rate between [0, 1]
        :param field_resolver: a map from field names defined in ``document`` (JSON, dict) to the field
            names defined in Protobuf. This is only used when the given ``document`` is
            a JSON string or a Python dict.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_csv
        async for r in self._get_client(**kwargs).search(
                _input_csv(lines,
                           size=size,
                           sampling_rate=sampling_rate,
                           field_resolver=field_resolver),
                on_done, on_error, on_always, data_type=DataInputType.AUTO, **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def search_lines(self,
                           lines: Union[Iterable[str], TextIO] = None,
                           filepath: str = None, size: int = None,
                           sampling_rate: float = None,
                           read_mode: str = 'r',
                           line_format: str = 'json',
                           field_resolver: Dict[str, str] = None,
                           on_done: CallbackFnType = None,
                           on_error: CallbackFnType = None,
                           on_always: CallbackFnType = None,
                           **kwargs):
        """ Use a list of files as the query source for searching on the current flow

        :param filepath: a text file that each line contains a document
        :param lines: a list of strings, each is considered as d document
        :param size: the maximum number of the documents
        :param sampling_rate: the sampling rate between [0, 1]
        :param read_mode: specifies the mode in which the file
                is opened. 'r' for reading in text mode, 'rb' for reading in binary
        :param line_format: the format of each line: ``json`` or ``csv``
        :param field_resolver: a map from field names defined in ``document`` (JSON, dict) to the field
            names defined in Protobuf. This is only used when the given ``document`` is
            a JSON string or a Python dict.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        from ...clients.sugary_io import _input_lines
        async for r in self._get_client(**kwargs).search(
                _input_lines(lines, filepath,
                             size=size,
                             sampling_rate=sampling_rate,
                             read_mode=read_mode,
                             line_format=line_format,
                             field_resolver=field_resolver),
                on_done, on_error, on_always, data_type=DataInputType.CONTENT,
                **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def index(self, input_fn: InputFnType,
                    on_done: CallbackFnType = None,
                    on_error: CallbackFnType = None,
                    on_always: CallbackFnType = None,
                    **kwargs):
        """Do indexing on the current flow

        It will start a :py:class:`CLIClient` and call :py:func:`index`.

        :param input_fn: An iterator of bytes. If not given, then you have to specify it in **kwargs**.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        async for r in self._get_client(**kwargs).index(input_fn, on_done, on_error, on_always, **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def update(self, input_fn: InputFnType,
                     on_done: CallbackFnType = None,
                     on_error: CallbackFnType = None,
                     on_always: CallbackFnType = None,
                     **kwargs):
        """Do updates on the current flow

        It will start a :py:class:`CLIClient` and call :py:func:`index`.

        :param input_fn: An iterator of bytes. If not given, then you have to specify it in **kwargs**.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        async for r in self._get_client(**kwargs).update(input_fn, on_done, on_error, on_always, **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def delete(self, ids: Iterable[str],
                     on_done: CallbackFnType = None,
                     on_error: CallbackFnType = None,
                     on_always: CallbackFnType = None,
                     **kwargs):
        """Do deletion on the current flow

        :param input_fn: An iterator of bytes. If not given, then you have to specify it in **kwargs**.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        async for r in self._get_client(**kwargs).delete(ids, on_done, on_error, on_always, **kwargs):
            yield r

    @deprecated_alias(buffer=('input_fn', 1), callback=('on_done', 1), output_fn=('on_done', 1))
    async def search(self, input_fn: InputFnType,
                     on_done: CallbackFnType = None,
                     on_error: CallbackFnType = None,
                     on_always: CallbackFnType = None,
                     **kwargs):
        """Do searching on the current flow

        It will start a :py:class:`CLIClient` and call :py:func:`search`.

        :param input_fn: An iterator of bytes. If not given, then you have to specify it in **kwargs**.
        :param on_done: the function to be called when the :class:`Request` object is resolved.
        :param on_error: the function to be called when the :class:`Request` object is rejected.
        :param on_always: the function to be called when the :class:`Request` object is  is either resolved or rejected.
        :param kwargs: accepts all keyword arguments of `jina client` CLI
        """
        async for r in self._get_client(**kwargs).search(input_fn, on_done, on_error, on_always, **kwargs):
            yield r
