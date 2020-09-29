__version__ = '0.5.0'
__author__ = 'idementyev@luxoft.com'
__date__ = '2020-09-28'


import os
import logging as log
import typing
import server.utils as utils
# from server.crypto import BaseCipher, AESCipher, RSACipher, HashAPI
from server.crypto import HashAPI


class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(
                SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class FileService(metaclass=SingletonType):
    """Singleton class with methods for working with file system."""
    __extension = None
    __directory = None

    # def __init__(self, *args, **kwargs):
    def __init__(self):
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
        _path = value
        if not os.path.isabs(value):
            _path = os.path.abspath(os.path.normpath(os.path.join(
                self.__directory, value)))

        if not os.path.exists(_path):
            log.error(f'Directory {_path} does not exist')
            raise FileNotFoundError(f'Directory {_path} does not exist')
        else:
            self.__directory = _path

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
            raise FileNotFoundError(f'File {_file} does not exist')

        return _file_data

    def get_file_data(self, filename: str, user_id: int = None) -> typing.Dict:
        """Get full info about file with content.

        Args:
            filename (str): Filename without .txt file extension.
            user_id: Id of user.
        Returns:
            _file_data_dict (dict): Dictionary with full info about file.
            Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                edit_date (str): date of last file modification.
                size (int): size of file in bytes.
        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            ValueError: if security level is invalid.
        """
        _file = f'{filename}.{self.__extension}'
        _file_full_path = os.path.join(self.path, _file)
        _file_content = None
        _file_data_dict = self.get_file_meta(_file_full_path)

        # no checks here because get_file_meta() already has them.
        with open(_file_full_path, 'r') as _fr:
            _file_content = _fr.read()
            log.debug(f'Data read from {_file} successfully.')
        _file_data_dict['content'] = _file_content
        return _file_data_dict

    async def get_file_data_async(self, filename: str,
                                  user_id: int = None) -> typing.Dict:
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

    # async def create_file(self, content: str = None,
    def create_file(self, content: str = None,
                    security_level: str = None,
                    user_id: int = None) -> typing.Dict:
        """Create new .txt file.

        Method generates name of file from random string with digits
        and latin letters.

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
        _file_name = utils.generate_string()
        _file = f'{_file_name}.{self.__extension}'
        _file_full_path = os.path.join(self.path, _file)

        # check for existing files with recursion
        while os.path.exists(_file_full_path):
            log.info(f'File with name {_file} exists, regenerating name.')
            _file_data = self.create_file(content, security_level)
            return _file_data
        else:
            with open(_file_full_path, 'w') as _of:
                _of.write(content if content else '')
                log.info(f'Data written to file {_file}')
            _file_data = FileService.get_file_data(self, _file_name)
            return _file_data

    def delete_file(self, filename: str):
        """Delete file.

        Args:
            filename (str): Filename without .txt file extension.
        Returns:
            Str with filename with .txt file extension.
        Raises:
            AssertionError: if file does not exist.
        """
        _file = f'{filename}.{self.__extension}'
        _file_full_path = os.path.join(self.path, _file)

        try:
            os.remove(_file_full_path)
        except FileNotFoundError as _e:
            log.error(f'File {_file} does not exist.')
            raise FileNotFoundError(f'File {_file} does not exist.')
        else:
            log.info(f'File {_file} removed successfully.')
        return _file_full_path

    @staticmethod
    def set_logging(log_level='INFO'):
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


class FileServiceSigned(FileService):
    """Singleton class with methods for working with file system
    and file signatures.
    """
    def __init__(self):
        super(FileServiceSigned, self).__init__()

    def get_file_data(
            self, filename: str, user_id: int = None) -> typing.Dict:
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
                size (int): size of file in bytes.
                user_id (int): user Id.
        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            signatures are not match, signature file does not exist.
            ValueError: if security level is invalid.
        """
        _file_data = super(FileServiceSigned, self).get_file_data(
            filename, user_id)
        md5_file_name = f"{_file_data['name']}.md5"

        if os.path.exists(md5_file_name):
            hashed_data = HashAPI.hash_md5(
                '__'.join(map(str, _file_data.values())))
            with open(md5_file_name) as md5file:
                if hashed_data == md5file.read():
                    return _file_data
                else:
                    log.error(f"Failed checksum on file {_file_data['name']}.")
                    return {}
        else:
            log.error(f"File {_file_data['name']} was not hashed on creation.")
            raise PermissionError(
                f"File {_file_data['name']} was not hashed on creation.")

    async def get_file_data_async(self, filename: str,
                                  user_id: int = None) -> typing.Dict:
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
                size (int): size of file in bytes.
                user_id (int): user Id.
        Raises:
            AssertionError: if file does not exist, filename format is invalid,
            signatures are not match, signature file does not exist.
            ValueError: if security level is invalid.
        """
        pass

    # async def create_file(self, content: str = None,
    def create_file(self, content: str = None,
                    security_level: str = None,
                    user_id: int = None) -> typing.Dict:
        """Create new .txt file with signature file.

        Method generates name of file from random string with digits
        and latin letters.

        Args:
            content (str): String with file content,
            security_level (str): String with security level,
            user_id (int): User Id.
        Returns:
            Dict, which contains name of created file. Keys:
                name (str): name of file with .txt extension.
                content (str): file content.
                create_date (str): date of file creation.
                size (int): size of file in bytes.
                user_id (int): user Id.
        Raises:
            AssertionError: if user_id is not set.
            ValueError: if security level is invalid.
        """
        created_dict = super(FileServiceSigned, self).create_file(
            content, security_level, user_id)
        hashed_data = HashAPI.hash_md5(
            '__'.join(map(str, created_dict.values())))

        md5_file_name = f"{created_dict['name']}.md5"
        md5_full_path = os.path.join(self.path, md5_file_name)

        with open(md5_full_path, 'w') as md5_file:
            md5_file.write(hashed_data)
        return created_dict

    def delete_file(self, filename: str):
        """Delete file.

        Args:
            filename (str): Filename without .txt file extension.
        Returns:
            Str with filename with .txt file extension.
        Raises:
            AssertionError: if file does not exist.
        """
        returned_string = super(FileServiceSigned, self).delete_file(filename)

        if returned_string:
            md5_file_name = f"{returned_string}.md5"
            try:
                os.remove(md5_file_name)
            except FileNotFoundError as _e:
                log.error(f'File {md5_file_name} does not exist.')
                return returned_string
            else:
                log.info(f'File {md5_file_name} removed successfully.')
        return returned_string


if __name__ == '__main__':
    fs = FileServiceSigned()
    fs.set_logging('DEBUG')
    fs.path = '.'
    original_path = fs.path
    fs.path = original_path

    # test file creation
    created = fs.create_file('Lorem Ipsum')
    created_file, _ext = os.path.splitext(created['name'])

    # test get_files
    print(fs.get_files())

    # test get_file_data
    print(fs.get_file_data(created_file))

    # test file deletion
    print(fs.delete_file(created_file))
