__version__ = '0.2.0'
__author__ = 'idementyev@luxoft.com'
__date__ = '2020-09-23'


import os
import server.utils as utils
import logging as log

extension = 'txt'


def change_dir(path):
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
    Raises:
        AssertionError: if directory does not exist.
    Returns:
        path (str): Current working directory.
    """
    try:
        os.chdir(path)
    except FileNotFoundError:
        log.error(f'Directory {path} does not exist')

    return os.getcwd()


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


def get_file_data(filename):
    """Get full info about file with content.

    Args:
        filename (str): Filename without .txt file extension.
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
    _file = f'{filename}.{extension}'
    _file_content = None
    _file_data_dict = get_file_meta(_file)

    # no checks here because get_file_meta() already has them.
    with open(_file, 'r') as _fr:
        _file_content = _fr.read()
        log.debug(f'Data read from {_file} successfully.')
    _file_data_dict['content'] = _file_content

    return _file_data_dict


def get_files(_directory=None):
    """Get info about all files in working directory.

    Args:
        _directory (str): Optional directory to list files from.
    Returns:
        _files_list (list): List of dicts with info about each file.
        Keys:
            name (str): name of file with .txt extension.
            create_date (str): date of file creation.
            edit_date (str): date of last file modification.
            size (int): size of file in bytes.
    """
    _directory = _directory if _directory else os.getcwd()
    _files_list = []

    for _r, _d, _files in os.walk(_directory):
        for _f in _files:
            _, _f_ext = os.path.splitext(_f)
            if _f_ext == f'.{extension}':
                _meta_file = os.path.join(_directory, _f)
                _meta_dict = get_file_meta(_meta_file)
                _files_list.append(_meta_dict)
        # only 1st level
        break

    return _files_list


def create_file(content=None, security_level=None):
    """Create new .txt file.

    Method generates name of file from random string with digits
    and latin letters.

    Args:
        content (str): String with file content,
        security_level (str): String with security level.
    Returns:
        _file (dict): Dictionary describing file.
        Keys:
            name (str): name of file with .txt extension.
            content (str): file content.
            create_date (str): date of file creation.
            size (int): size of file in bytes.
            user_id (int): user id.  TODO: add?
    Raises:
        AssertionError: if user_id is not set.
        ValueError: if security level is invalid.
    """
    _file_name = utils.generate_string()
    _file = f'{_file_name}.{extension}'

    # check for existing files with recursion
    while os.path.exists(_file):
        log.info(f'File with name {_file} exists, regenerating name.')
        _file_data = create_file(content, security_level)
        return _file_data
    else:
        with open(_file, 'w') as _of:
            _of.write(content if content else '')
            log.info(f'Data written to file {_file}')
        _file_data = get_file_data(_file_name)
        return _file_data


def delete_file(filename):
    """Delete file in current working directory.

    Args:
        filename (str): Filename without .txt file extension.
    Returns:
        _file (str): Filename with .txt file extension.
    Raises:
        AssertionError: if file does not exist.
    """
    _file = f'{filename}.{extension}'
    try:
        os.remove(_file)
    except FileNotFoundError as _e:
        log.error(f'File {_file} does not exist.')
        return None
    else:
        log.info(f'File {_file} removed successfully.')
    return _file


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


if __name__ == '__main__':
    # test change_dir
    print(f"new directory: {change_dir('..')}")

    # test file creation
    created = create_file('Lorem Ipsum')
    created_file, _ext = os.path.splitext(created['name'])

    # test get_files
    print(get_files('.'))

    # test get_file_data
    print(get_file_data(created_file))

    # test file deletion
    print(delete_file(created_file))
