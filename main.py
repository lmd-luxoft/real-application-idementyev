__version__ = '0.2.0'
__author__ = 'idementyev@luxoft.com'
__date__ = '2020-09-23'


import argparse
import os
# import sys
# import logging
# import json
# from aiohttp import web
# from server.handler import Handler
# from server.database import DataBase
# from server.file_service import FileService, FileServiceSigned
import server.file_service
# import server.file_service_no_class as file_service


def commandline_parser() -> argparse.ArgumentParser:
    """Command line parser.

    Get and parse command line parameters and configure web app.
    Command line options:
    -p --port      - port (default: 8080).
    -d --directory - working directory (absolute or relative path,
                     default: current app folder FileServer).
    -i --init      - initialize database.
    -h --help      - help.
    """
    # noinspection PyTypeChecker
    # (broken in PyCharm 2020.x)
    p = argparse.ArgumentParser(
        description='Some app that does something, which I cannot yet name, '
                    'but eventually it \nwill work with files, so let\'s call '
                    'it next-next-cloud.',
        epilog="v{} ({}) by {}".format(__version__, __date__,
                                       __author__),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('-p', '--port', type=int, metavar='PORT', default=8080,
                   help='port for application')
    p.add_argument('-d', '--directory', metavar='DIR', type=str, default=None,
                   help='working directory')
    p.add_argument('-i', '--init', action='store_true', default=False,
                   help='initialize database')
    # either verbose or quiet, can be default
    g1 = p.add_mutually_exclusive_group(required=False)
    g1.add_argument('-v', '--verbose', action='store_true', default=False,
                    help='verbose output')
    g1.add_argument('-q', '--quiet', action='store_true', default=False,
                    help='display warnings and errors only')
    return p


def get_file_data(_file=None):
    """Get full info about file with content.

    Args:
        _file (str): Filename without .txt file extension.
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
    if not _file:
        print("Enter file name:")
        _file = input(f'file:{cli_prompt}')
    _file_obj = file_service.get_file_data(_file)

    return _file_obj


def create_file(_content=None):
    """Create new .txt file.

    Method generates name of file from random string with digits
    and latin letters.

    Args:
        _content (str): String with file content,
    Returns:
        _file (dict): Dictionary describing file.
        Keys:
            name (str): name of file with .txt extension.
            content (str): file content.
            create_date (str): date of file creation.
            size (int): size of file in bytes,
            user_id (int): user Id.
    Raises:
        AssertionError: if user_id is not set,
        ValueError: if security level is invalid.
    """
    if not _content:
        print("Enter file contents:")
        _content = input(f'text:{cli_prompt}')
    _file = file_service.create_file(_content)
    return _file


def delete_file(_path=None):
    """Delete file in current working directory.

    Args:
        _path (str): Filename without .txt file extension.
    Returns:
        _file (str): Filename with .txt file extension.
    Raises:
        AssertionError: if file does not exist.
    """
    if not _path:
        print("Enter file to remove (no extensions):")
        _path = input(f'file:{cli_prompt}')
    _file = file_service.delete_file(_path)
    return _file


def change_dir(_path=None):
    """Change working directory.

    Args:
        _path (str): Working directory path.
    Returns:
        _new_dir (str): New working directory.
    """

    if not _path:
        print("Enter directory:")
        _path = input(f'path:{cli_prompt}')
    try:
        file_service.path = _path
    except FileNotFoundError:
        pass
    else:
        print(file_service.path)


def main():
    """Entry point of app."""
    args, _ = commandline_parser().parse_known_args()

    # check passed verbosity against default value
    if args.verbose:
        log_level = 'DEBUG'
    elif args.quiet:
        log_level = 'WARNING'
    else:
        log_level = 'INFO'

    # initialize logging in the 'file_service' module
    file_service.set_logging(log_level)

    if args.directory:
        _pwd = change_dir(args.directory)
        server.file_service.log.info(f"Directory set to {_pwd}.")

    # run CLI
    cli()


def cli_help():
    """
    Display command list for CLI with pretty formatting.
    """
    cli_commands_help = {
        'cd': 'change current directory',
        'pwd': 'print current directory',
        'list': 'get files in current directory',
        'get': 'get file contents',
        'create': 'create file',
        'delete': 'delete file (no extension)',
        'help': 'print this message',
        'exit': 'exit CLI'
    }

    print("Command list:")
    for k, v in cli_commands_help.items():
        print(f'{k:8} - {v}')


def cli():
    """
    Make simple CLI infinite cycle with... hope that they won't hack us =(
    Don't do this. Never.
    """
    cli_help()

    while True:
        command = input(cli_prompt)

        if command == 'cd':
            change_dir()
            continue
        if command == 'pwd':
            print(os.getcwd())
        elif command == 'list':
            files = file_service.get_files()
            for f in files:
                print(f['name'])
        elif command == 'get':
            print(f"{get_file_data()['content']}")
            continue
        elif command == 'create':
            print(f"Created file: {create_file()['name']}")
            continue
        elif command == 'delete':
            print(f"Deleted file: {delete_file()}")
            continue
        elif command == 'help':
            cli_help()
        elif command == 'exit':
            return
        elif not command:
            continue
        else:
            print("Unrecognized command, try again.")


if __name__ == '__main__':
    cli_prompt = '> '
    file_service = server.file_service.FileService()
    main()
