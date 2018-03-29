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
$ find . -type f -name "*.html" \
    -exec replace \
      -f 'http://example.com' \
      -t 'https://example.com' \
      -i {} \;
```