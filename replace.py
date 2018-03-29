#!/usr/bin/env python3
# Generic search & replace tool
# Aurelio Jargas, 2016-08-13
#
# See also https://github.com/dmerejkowsky/replacer/blob/master/bin/replacer

"""
Examples:
    # Replace all mentions of old.css with new.css in all HTML files
    replace --from old.css --to new.css --in-place *.html

    # Update the AdSense code in all HTML files
    # The old and the new code are in separate files
    replace --from-file adsense.old --to-file adsense.new -i *.html

    # Enclose all numbers inside square brackets: 123 -> [123]
    replace --regex --from '(\\d+)' --to '[\\1]' file.txt
"""

import sys
import re
import argparse

# XXX Maybe use that instead of reading the file manually?
# >>> parser = argparse.ArgumentParser()
# >>> parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
# ...                     default=sys.stdin)
# >>> parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
# ...                     default=sys.stdout)
# >>> parser.parse_args(['input.txt', 'output.txt'])
# Namespace(infile=<_io.TextIOWrapper name='input.txt' encoding='UTF-8'>,
#           outfile=<_io.TextIOWrapper name='output.txt' encoding='UTF-8'>)
# >>> parser.parse_args([])
# Namespace(infile=<_io.TextIOWrapper name='<stdin>' encoding='UTF-8'>,
#           outfile=<_io.TextIOWrapper name='<stdout>' encoding='UTF-8'>)


def read_file(path):
    with open(path, 'r') as myfile:
        return myfile.read()


def parse_cmdline():
    parser = argparse.ArgumentParser(
        description='Replaces text using string or regex matching.',
        epilog=__doc__,  # module docstring

        # avoid line wrapping on the epilog text
        # https://docs.python.org/3/library/argparse.html#formatter-class
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # from
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--from', metavar='TEXT', dest='from_',
                       help='specify the search text or regex')
    group.add_argument('-F', '--from-file', metavar='FILE',
                       help='read the search text from this file')
    # to
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--to', metavar='TEXT',
                       help='specify the replacement text')
    group.add_argument('-T', '--to-file', metavar='FILE',
                       help='read the replacement text from this file')
    # other
    parser.add_argument('-r', '--regex', action='store_true',
                        help='use regex matching instead of string matching')

    parser.add_argument('-i', '--in-place', action='store_true',
                        help='edit files in-place')
    # files
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='input files')
    return parser.parse_args()


config = parse_cmdline()
# print(args); sys.exit(0) # debug

# Set search pattern
if config.from_file:
    from_ = read_file(config.from_file)
elif config.from_:
    from_ = config.from_
else:
    print('Error: No search pattern (use --from or --from-file)')
    sys.exit(1)

# Set replacement
if config.to_file:
    to_ = read_file(config.to_file)
elif config.to is not None:  # could also be ''
    to_ = config.to
else:
    print('Error: No replace pattern (use --to or --to-file)')
    sys.exit(1)

for input_file in config.files:
    original = read_file(input_file)

    if config.regex:
        modified = re.sub(from_, to_, original)
    else:
        modified = original.replace(from_, to_)

    if config.in_place:

        # do not save unchanged files
        if modified == original:
            continue

        f = open(input_file, 'w')
        f.write(modified)
        f.close()
        print('Saved %s' % input_file)
    else:
        print(modified)
