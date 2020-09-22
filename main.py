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

    pass


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


def delete_file(path):
    """Delete file.

    Args:
        path (str): Working directory path.

    Returns:
        Str with filename with .txt file extension.

    Raises:
        AssertionError: if file does not exist.

    """

    pass


def change_dir(path):
    """Change working directory.

    Args:
        path (str): Working directory path.

    Returns:
        Str with successfully result.

    """

    pass


def main():
    """Entry point of app.

    Get and parse command line parameters and configure web app.
    Command line options:
    -p --port - port (default: 8080).
    -f --folder - working directory (absolute or relative path, default: current app folder FileServer).
    -i --init - initialize database.
    -h --help - help.

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
    args, _ = p.parse_known_args()

    if args.directory:
        FileServiceNoClass.change_dir(args.directory)

    # run CLI
    cli()


def cli():
    """
    Make simple CLI infinite cycle with... hope that they won't hack us =(
    Don't do this. Never.
    """

    prompt = '> '

    print("cd     - change dir")
    print("pwd    - print current dir")
    print("list   - get files in dir")
    print("get    - get files contents")
    print("create - create file")
    print("delete - delete file (no extension)")
    print("Enter 'exit' to, well, exit.")

    while True:
        command = input(prompt)

        if command == 'cd':
            print("Enter directory:")
            input_cd = input(f'cd:{prompt}')
            FileServiceNoClass.change_dir(input_cd)
        if command == 'pwd':
            print(os.getcwd())
        elif command == 'list':
            files = FileServiceNoClass.get_files()
            for f in files:
                print(f['name'])
        elif command == 'get':
            print("Enter file name:")
            input_get = input(f'file:{prompt}')
            file_obj = FileServiceNoClass.get_file_data(input_get)
            print(file_obj['content'])
        elif command == 'create':
            print("Enter file contents:")
            input_contents = input(f'text:{prompt}')
            file_obj = FileServiceNoClass.create_file(input_contents)
            print(f"Created file {file_obj['name']}")
        elif command == 'delete':
            print("Enter file to remove (no extensions):")
            input_remove = input(f'file:{prompt}')
            print(FileServiceNoClass.delete_file(input_remove))
        elif command == 'exit':
            return
        else:
            print("Unrecognized command, try again.")


if __name__ == '__main__':
    main()
