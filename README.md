## To do

- Make it easier to santize custom stuff.
- Sanitization is pretty simple, it should really only match on whole words (not inside words).
- Try it on some other code.
- Run it on a single file or on a folder?
- Make the output cleaner.
- Make it easier to identify things that need to be sanitized.
- Make it possible to santize by removing a whole line.

## Things to sanitize
These are non-standard C things used by the target compiler.

- Remove `interrupt` keywords.
- Remove @(blah) statements.
- Remove `*far`.