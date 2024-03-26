#!/usr/bin/env python3
# Generic search & replace tool
# Aurelio Jargas, 2016-08-13

"""
Replaces text using string or regex matching.

Examples:
  # Replace all mentions of old.css with new.css in all HTML files
  replace --from old.css --to new.css --in-place *.html

  # Update the AdSense code in all HTML files
  # The old and the new code are in separate files
  replace --from-file adsense.old --to-file adsense.new -i *.html

  # Enclose all numbers inside square brackets: 123 -> [123]
  replace --regex --from '(\\d+)' --to '[\\1]' file.txt
"""

import argparse
import pathlib
import re
import sys


# read/write files using bytes to avoid line break issues
def read_file(path):
    if str(path) == '-':
        return sys.stdin.read()
    return path.read_bytes().decode(encoding='utf-8')


def save_file(path, content):
    path.write_bytes(bytes(content, encoding='utf-8'))


def setup_cmdline_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # from
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-f',
        '--from',
        metavar='TEXT',
        dest='from_',
        help='specify the search text or regex',
    )
    group.add_argument(
        '-F',
        '--from-file',
        metavar='FILE',
        type=pathlib.Path,
        help='read the search text from this file',
    )

    # to
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-t',
        '--to',
        metavar='TEXT',
        help='specify the replacement text',
    )
    group.add_argument(
        '-T',
        '--to-file',
        metavar='FILE',
        type=pathlib.Path,
        help='read the replacement text from this file',
    )

    # other
    parser.add_argument(
        '-r',
        '--regex',
        action='store_true',
        help='use regex matching instead of string matching',
    )
    parser.add_argument(
        '-i',
        '--in-place',
        action='store_true',
        help='edit files in-place',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='turn on verbose mode',
    )

    # files
    parser.add_argument(
        'files',
        metavar='FILE',
        nargs='+',
        type=pathlib.Path,
        help='input files',
    )
    return parser


def validate_config(config):
    # Set search pattern
    if config.from_file:
        config.from_value = read_file(config.from_file)
    elif config.from_:
        config.from_value = config.from_
    else:
        sys.exit('Error: No search pattern (use --from or --from-file)')

    # Set replacement
    if config.to_file:
        config.to_value = read_file(config.to_file)
    elif config.to is not None:  # could also be ''
        config.to_value = config.to
    else:
        sys.exit('Error: No replace pattern (use --to or --to-file)')


def replace(from_, to_, text, use_regex):
    if use_regex:
        return re.sub(from_, to_, text)
    return text.replace(from_, to_)


def main(args=None):
    parser = setup_cmdline_parser()
    config = parser.parse_args(args)
    validate_config(config)

    from_ = config.from_value
    to_ = config.to_value

    for input_file in config.files:
        if config.verbose:
            print('----', input_file)

        original = read_file(input_file)
        modified = replace(from_, to_, original, config.regex)

        # save or show results
        if config.in_place:
            if modified == original:
                continue  # do not save unchanged files
            save_file(input_file, modified)
            print('Saved', input_file)
        else:
            print(modified, end='')


if __name__ == '__main__':
    main()
