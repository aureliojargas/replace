# replace

Generic file search & replace tool, written in Python 3.

## Options

Specify the FROM/TO patterns directly in the command line:

```
-f, --from TEXT         specify the search text or regex
-t, --to TEXT           specify the replacement text
```

Specify the FROM/TO patterns using files, useful for multiline matches:

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

First, setup a sample text file:

```console
$ echo 'the quick brown fox' > file.txt
$ cat file.txt
the quick brown fox
$
```

Now we'll do some replaces using string matching, which is the default. Note that there are short and long options (`-f`/`--from`) and that the replacement is performed globally: all occurrences are replaced.

```console
$ ./replace.py --from 'brown' --to 'red' file.txt
the quick red fox
$ ./replace.py -f 'brown' -t 'red' file.txt
the quick red fox
$ ./replace.py -f 'o' -t '◆' file.txt
the quick br◆wn f◆x
$
```

For more powerfull searches, use `-r` or `--regex` to perform a regular expression match. You have access to the full power of Python's regex flavor.

```console
$ ./replace.py --regex -f '[aeiou]' -t '◆' file.txt
th◆ q◆◆ck br◆wn f◆x
$ ./replace.py -r -f '[aeiou]' -t '◆' file.txt
th◆ q◆◆ck br◆wn f◆x
$
```

If necessary, you can also apply the replacements on text coming from STDIN, using `-` as the file name.

```console
$ cat file.txt | ./replace.py -r -f '[aeiou]' -t '◆' -
th◆ q◆◆ck br◆wn f◆x
$
```

Note that all the previous replaces were not saved to the original file. This is the default behavior (just like `sed`). If you want to edit the original file, use the `-i` or `--in-place` options:

```console
$ ./replace.py -r -f '[aeiou]' -t '◆' -i file.txt
Saved file.txt
$ cat file.txt
th◆ q◆◆ck br◆wn f◆x
$
```

Some boring tests for missing or incomplete command line options:

```console
$ ./replace.py 2>&1 | grep error
replace.py: error: the following arguments are required: FILE
$ ./replace.py README.md
Error: No search pattern (use --from or --from-file)
$ ./replace.py -f '' README.md
Error: No search pattern (use --from or --from-file)
$ ./replace.py -f foo README.md
Error: No replace pattern (use --to or --to-file)
$
```

OK, we're done for now.

```console
$ rm file.txt
$
```

## Similar tools

- https://github.com/dmerejkowsky/replacer/
- https://github.com/facebook/codemod
