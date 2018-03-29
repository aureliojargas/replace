# replace

Generic file search & replace tool, written in Python 3.

## Options

Specify the FROM/TO patterns directly in the command line:

```
-f, --from TEXT         specify the search text or regex
-t, --to TEXT           specify the replacement text
```

Specify the FROM/TO patterns using files:

```
-F, --from-file FILE    read the search text from this file
-T, --to-file FILE      read the replacement text from this file
```

The default search uses simple string matching, no magic.
But if you need power, there you have it:

```
-r, --regex             use regex matching instead of string matching
```

Just like `sed`, this script by default show results to STDOUT.
But instead, you can save the edits to the original file:

```
-i, --in-place          edit files in-place
```


## Examples

```bash
# Replace all mentions of old.css with new.css in all HTML files
replace --from old.css --to new.css --in-place *.html

# Update the AdSense code in all HTML files
# The old and the new code are in separate files
replace --from-file adsense.old --to-file adsense.new -i *.html

# Enclose all numbers inside square brackets: 123 -> [123]
replace --regex --from '(\d+)' --to '[\\1]' file.txt

# From http to https in all HTML files, recursive
find . -type f -name "*.html" \
    -exec replace \
      -f 'http://example.com' \
      -t 'https://example.com' \
      -i {} \;
```

## Tests

The following command lines are executed and verified by [clitest](https://github.com/aureliojargas/clitest), using the `clitest README.md` command.

```console
$ echo 'the quick brown fox' > file.txt
$ cat file.txt
the quick brown fox
$ ./replace.py --from 'brown' --to 'red' file.txt
the quick red fox
$ ./replace.py -f 'brown' -t 'red' file.txt
the quick red fox
$ ./replace.py -f 'o' -t '◆' file.txt
the quick br◆wn f◆x
$ ./replace.py --regex -f '[aeiou]' -t '◆' file.txt
th◆ q◆◆ck br◆wn f◆x
$ ./replace.py -r -f '[aeiou]' -t '◆' file.txt
th◆ q◆◆ck br◆wn f◆x
$ rm file.txt
$
```

Command line options missing or incomplete:

```console
$ ./replace.py
usage: replace.py [-h] [-f TEXT | -F FILE] [-t TEXT | -T FILE] [-r] [-i] FILE [FILE ...]
replace.py: error: the following arguments are required: FILE
$ ./replace.py README.md
Error: No search pattern (use --from or --from-file)
$ ./replace.py -f '' README.md
Error: No search pattern (use --from or --from-file)
$ ./replace.py -f foo README.md
Error: No replace pattern (use --to or --to-file)
$
```
