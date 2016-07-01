import locale
import argparse
import os
import sys

from asciinema import __version__
from asciinema.commands.record import RecordCommand
from asciinema.commands.auth import AuthCommand
from asciinema.config import Config
from asciinema.api import Api

def auth(args, config):
    return AuthCommand(config.api_url, config.api_token)

def rec(args, config):
    api = Api(config.api_url, os.environ.get("USER"), config.api_token)
    return RecordCommand(api, args.filename, args.command, args.title, args.yes)

def main():
    if locale.nl_langinfo(locale.CODESET).upper() != 'UTF-8':
        print("asciinema needs a UTF-8 native locale to run. Check the output of `locale` command.")
        sys.exit(1)

    # create the top-level parser
    parser = argparse.ArgumentParser(
        description="Record and share your terminal sessions, the right way.",
        epilog="""example usage:
  Record terminal and upload it to asciinema.org:
    \x1b[1masciinema rec\x1b[0m
  Record terminal to local file:
    \x1b[1masciinema rec demo.json\x1b[0m

For help on a specifc command run:
  \x1b[1masciinema <command> -h\x1b[0m""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', help='show version information', action='store_true')

    subparsers = parser.add_subparsers()

    # create the parser for the "auth" command
    parser_auth = subparsers.add_parser('auth', help='Assign local API token to asciinema.org account')
    parser_auth.set_defaults(func=auth)

    # create the parser for the "rec" command
    parser_rec = subparsers.add_parser('rec', help='Record terminal session')
    parser_rec.add_argument('-c', '--command', help='command to record, defaults to $SHELL')
    parser_rec.add_argument('-t', '--title', help='title of the asciicast')
    parser_rec.add_argument('-y', '--yes', help='answer "yes" to all prompts (e.g. upload confirmation)', action='store_true')
    parser_rec.add_argument('filename', nargs='?', default='')
    parser_rec.set_defaults(func=rec)

    # parse the args and call whatever function was selected
    args = parser.parse_args()

    if args.version:
        print('asciinema %s' % __version__)
    else:
        if hasattr(args, 'func'):
            command = args.func(args, Config())
            code = command.execute()
            sys.exit(code)
        else:
            parser.print_help()


if __name__ == '__main__':
    main()
