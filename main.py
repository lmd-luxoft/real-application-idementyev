__version__ = '0.1.0'
__author__ = 'idementyev@luxoft.com'
__date__ = '2020-09-22'


import argparse as ap
import os
import sys
import logging
import json
from aiohttp import web
from server.handler import Handler
#from server.database import DataBase
from server.file_service import FileService, FileServiceSigned
import server.file_service_no_class as FileServiceNoClass


def commandline_parser() -> ap.ArgumentParser:
    """Command line parser.

    Parse port and working directory parameters from command line.

    """
    p = ap.ArgumentParser(
        description='Some app that does something, which I cannot yet name,\n'
                    'but eventually it will work with files, so let\'s call '
                    'it the nextnextcloud.',
        epilog="v{} ({}) by {}".format(__version__, __date__,
                                       __author__),
        formatter_class=ap.RawDescriptionHelpFormatter)
    p.add_argument('-p', '--port', type=int, metavar='PORT', default=8080,
                   help='port for application')
    # p.add_argument('-f', '--folder', type=str, default='.',
    #                help='working directory')
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


def get_file_data(path):
    """Get full info about file.

    Args:
        path (str): Working directory path.

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

    pass


def create_file(path):
    """Create new .txt file.

    Method generates name of file from random string with digits and latin letters.

    Args:
        path (str): Working directory path.

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
    _file = FileServiceNoClass.delete_file(_path)
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
    _new_dir = FileServiceNoClass.change_dir(_path)
    return _new_dir


def main():
    """Entry point of app.

    Get and parse command line parameters and configure web app.
    Command line options:
    -p --port - port (default: 8080).
    -f --folder - working directory (absolute or relative path, default: current app folder FileServer).
    -i --init - initialize database.
    -h --help - help.

    """

    args, _ = commandline_parser().parse_known_args()

    if args.directory:
        _pwd = change_dir(args.directory)
        print(f"Directory changed to {_pwd}.")

    # run CLI
    cli()


def cli():
    """
    Make simple CLI infinite cycle with... hope that they won't hack us =(
    Don't do this. Never.
    """

    print("cd     - change dir")
    print("pwd    - print current dir")
    print("list   - get files in dir")
    print("get    - get files contents")
    print("create - create file")
    print("delete - delete file (no extension)")
    print("Enter 'exit' to, well, exit.")

    while True:
        command = input(cli_prompt)

        if command == 'cd':
            print(change_dir())
            continue
        if command == 'pwd':
            print(os.getcwd())
        elif command == 'list':
            files = FileServiceNoClass.get_files()
            for f in files:
                print(f['name'])
        elif command == 'get':
            print("Enter file name:")
            input_get = input(f'file:{cli_prompt}')
            file_obj = FileServiceNoClass.get_file_data(input_get)
            print(file_obj['content'])
            continue
        elif command == 'create':
            print("Enter file contents:")
            input_contents = input(f'text:{cli_prompt}')
            file_obj = FileServiceNoClass.create_file(input_contents)
            print(f"Created file: {file_obj['name']}")
            continue
        elif command == 'delete':
            print(f"Deleted file: {delete_file()}")
            continue
        elif command == 'exit':
            return
        else:
            print("Unrecognized command, try again.")


if __name__ == '__main__':
    cli_prompt = '> '

    main()
