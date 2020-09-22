# Copyright 2020 by Kirill Kanin, Ilya Dementyev
# All rights reserved.


import os
import sys
import server.utils as utils

extension = 'txt'


def change_dir(path):
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.

    Raises:
        AssertionError: if directory does not exist.

    """

    if not os.path.exists(path):
        raise AssertionError(f'Directory {path} does not exist')
    else:
        os.chdir(path)
        print(f'Dir changed to {path}')


def get_file_data(filename):
    """Get full info about file.

    Args:
        filename (str): Filename without .txt file extension.

    Returns:
        Dict, which contains full info about file. Keys:
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

    if not os.path.exists(_file):
        raise AssertionError(f'File {_file} does not exist')

    try:
        with open(_file, 'r') as _fr:
            _file_content = _fr.read()
    except OSError as _e:
        #if _e.errno ==
        # TODO: get proper 'EPERM' here
        raise _e

    # file exists here
    _file_stat = os.stat(_file)

    _file_data_dict = {
        'name': None,
        'content': None,
        'create_date': None,
        'edit_date': None,
        'size': None,
    }

    _file_data_dict['name'] = os.path.basename(_file)
    _file_data_dict['content'] = _file_content
    # TODO: this is heavy, make properly cross-platform
    _file_data_dict['create_date'] = _file_stat.st_ctime
    _file_data_dict['edit_date'] = _file_stat.st_mtime
    _file_data_dict['size'] = _file_stat.st_size

    return _file_data_dict


def get_files(_directory=None):
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
            name (str): name of file with .txt extension.
            create_date (str): date of file creation.
            edit_date (str): date of last file modification.
            size (str): size of file in bytes.

    """

    _directory = _directory if _directory else os.getcwd()
    _files_list = []

    for _r, _d, _files in os.walk(_directory):
        for _f in _files:
            _f_dict = {}
            _f_path, _f_ext = os.path.splitext(_f)
            if _f_ext == f'.{extension}':
                _input_file = os.path.join(_directory, _f_path)

                # make dictionary
                # I am lazy so I reuse the code and save everything
                # without content
                # TODO: don't be lazy, make a function without content!
                _full_dict = get_file_data(_input_file)
                _f_dict = {_i: _full_dict[_i] for _i in _full_dict if _i != 'content'}

                _files_list.append(_f_dict)

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
    _file = f'{_file_name}.{extension}'

    with open(_file, 'w') as _of:
        _of.write(content if content else '')

    return get_file_data(_file_name)


def delete_file(filename):
    """Delete file.

    Args:
        filename (str): Filename without .txt file extension.

    Returns:
        Str with filename with .txt file extension.

    Raises:
        AssertionError: if file does not exist.

    """

    _file = f'{filename}.{extension}'
    if not os.path.exists(_file):
        raise AssertionError(f'File {_file} does not exist')

    try:
        os.remove(_file)
    except OSError as _e:
        # TODO: again, proper catch should be implemented here
        raise _e

    return _file


# test chdir
change_dir('..')

# test get_file_data
print(get_file_data('requirements'))

# test get_files
print(get_files('.'))

# test file creation
created = create_file('Lorem Ipsum')
created_file, _ext = os.path.splitext(created['name'])

# test file deletion
print(delete_file(created_file))
