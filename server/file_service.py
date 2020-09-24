# Copyright 2019 by Kirill Kanin.
# All rights reserved.

import os
import logging as log
import typing
import server.utils as utils
from collections import OrderedDict
from server.crypto import BaseCipher, AESCipher, RSACipher, HashAPI


class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class FileService(metaclass=SingletonType):
    """Singleton class with methods for working with file system."""

    # def __new__(cls, *args, **kwargs):
    #     pass

    __extension = None
    __directory = None

    def __init__(self, *args, **kwargs):
        self.__extension = 'txt'
        self.__directory = '.'

    @property
    def path(self) -> str:
        """Working directory path getter.

        Returns:
            Str with working directory path.
        """
        return self.__directory

    @path.setter
    def path(self, value: str):
        """Working directory path setter.

        Args:
            value (str): Working directory path.
        """
        if os.path.isabs(value):
            self.__directory = value
        else:
            self.__directory = os.path.abspath(
                os.path.normpath(
                    os.path.join(self.__directory, value)))

    @staticmethod
    def get_file_meta(_file):
        """Get meta info about file.

        Args:
            _file (str): Filename with file extension.
        Returns:
            _file_data (dict): Meta info about file.
            Keys:
                name (str): name of file with .txt extension.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes.
        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            ValueError: if security level is invalid.
        """
        _file_data = {}

        try:
            _file_stat = os.stat(_file)
            _file_data['name'] = os.path.basename(_file)
            _file_data['size'] = _file_stat.st_size
            _file_data['create_date'] = utils.convert_date(_file_stat.st_ctime)
            _file_data['edit_date'] = utils.convert_date(_file_stat.st_mtime)
        except FileNotFoundError as _e:
            log.error(f'File {_file} does not exist')

        return _file_data

    def get_file_data(self, filename: str, user_id: int = None) -> typing.Dict:
        """Get full info about file.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            ValueError: if security level is invalid.

        """

        pass

    async def get_file_data_async(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file. Asynchronous version.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            ValueError: if security level is invalid.

        """

        pass

    def get_files(self) -> typing.List[typing.Dict[str, str]]:
        """Get info about all files in working directory.

        Returns:
            List of dicts, which contains info about each file. Keys:
                name (str): name of file with .txt extension.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (str): size of file in bytes.

        """
        _files_list = []

        for _r, _d, _files in os.walk(self.__directory):
            for _f in _files:
                _, _f_ext = os.path.splitext(_f)
                if _f_ext == f'.{self.__extension}':
                    _meta_file = os.path.join(self.__directory, _f)
                    _meta_dict = self.get_file_meta(_meta_file)
                    _files_list.append(_meta_dict)
            # only 1st level
            break

        return _files_list

    async def create_file(
            self, content: str = None, security_level: str = None, user_id: int = None) -> typing.Dict[str, str]:
        """Create new .txt file.

        Method generates name of file from random string with digits and latin letters.

        Args:
            content (str): String with file content,
            security_level (str): String with security level,
            user_id (int): User Id.

        Returns:
            Dict, which contains name of created file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if user_id is not set,
            ValueError: if security level is invalid.

        """

        pass

    def delete_file(self, filename: str):
        """Delete file.

        Args:
            filename (str): Filename without .txt file extension.

        Returns:
            Str with filename with .txt file extension.

        Raises:
            AssertionError: if file does not exist.

        """

        pass


class FileServiceSigned(FileService):
    """Singleton class with methods for working with file system and file signatures.

    """

    def get_file_data(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid, signatures are not match,
            signature file does not exist,
            ValueError: if security level is invalid.

        """

        pass

    async def get_file_data_async(self, filename: str, user_id: int = None) -> typing.Dict[str, str]:
        """Get full info about file. Asynchronous version.

        Args:
            filename (str): Filename without .txt file extension,
            user_id (int): User Id.

        Returns:
            Dict, which contains full info about file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if file does not exist, filename format is invalid, signatures are not match,
            signature file does not exist,
            ValueError: if security level is invalid.

        """

        pass

    async def create_file(
            self, content: str = None, security_level: str = None, user_id: int = None) -> typing.Dict[str, str]:
        """Create new .txt file with signature file.

        Method generates name of file from random string with digits and latin letters.

        Args:
            content (str): String with file content,
            security_level (str): String with security level,
            user_id (int): User Id.

        Returns:
            Dict, which contains name of created file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                size (int): size of file in bytes,
                user_id (int): user Id.

        Raises:
            AssertionError: if user_id is not set,
            ValueError: if security level is invalid.

        """

        pass

    def set_logging(self, log_level='INFO'):
        """Set logging level.

        Logging level is passed from main.py or default INFO level is used.
        """
        log_format = '%(asctime)s %(levelname)s %(message)s'

        # override long names with short ones
        for level, letter in zip((10, 20, 30, 40, 50), 'DIWEC'):
            # noinspection PyTypeChecker
            # (broken in PyCharm 2020.x)
            log.addLevelName(level, letter)
        log.basicConfig(format=log_format, level=log_level)
        log.debug('Log level set to {lvl}'.format(lvl=log_level))


if __name__ == '__main__':
    fs = FileService()
    print(fs.path)

    fs.path = '..'
    print(fs.path)

    fs.path = '/home'
    print(fs.path)

    fs.path = '/home/rez/python/script-007'

    # test get_files
    print(fs.get_files())
