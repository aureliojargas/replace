#!/usr/bin/env python3
# Aurelio Jargas, 2016-08-13
#
# See also https://github.com/dmerejkowsky/replacer/blob/master/bin/replacer
#
# TODO:
# - keep original line break (\n or \r\n)

import sys
import re
import string
import argparse

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


parser = argparse.ArgumentParser(
    description='Replaces text using string or regex matching.',
    # epilog='Ending text.'
)

parser.add_argument('-F', '--from-file', metavar='FILE')
parser.add_argument('-f', '--from',      metavar='TEXT', dest='from_')
parser.add_argument('-T', '--to-file',   metavar='FILE')
parser.add_argument('-t', '--to',        metavar='TEXT')

parser.add_argument('-r', '--regex', action='store_true')
parser.add_argument('-i', '--in-place', action='store_true')

parser.add_argument(
    'files',
    metavar='FILE',
    nargs='+',
    help='input files')

args = parser.parse_args()
# print(args); sys.exit(0) # debug


def read_file(path):
    with open(path, 'r') as myfile:
        return myfile.read()

# Set search pattern
if args.from_file:
    from_ = read_file(args.from_file)
elif args.from_:
    from_ = args.from_
else:
    print('Error: No search pattern (use --from or --from-file)')
    sys.exit(1)

# Set replacement
if args.to_file:
    to_ = read_file(args.to_file)
elif args.to is not None:  # could also be ''
    to_ = args.to
else:
    print('Error: No replace pattern (use --to or --to-file)')
    sys.exit(1)

for input_file in args.files:
    original = read_file(input_file)

    if args.regex:
        modified = re.sub(from_, to_, original)
    else:
        modified = original.replace(from_, to_)

    if args.in_place:

        # do not save unchanged files
        if modified == original:
            continue

        f = open(input_file, 'w')
        f.write(modified)
        f.close()
        print("Saved %s" % input_file)
    else:
        print(modified)
