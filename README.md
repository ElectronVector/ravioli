# Ravioli

A tool for calculating simple, useful complexity metrics for C.

This tool is designed to work especially on embedded software written for compilers with non-standard extensions.
It works without a compiler or any preprocessing required.

## To do

- Implementing a simpler parsing that doesn't require complete preprocessing.
 - Add counting of compound conditional.
 - Add a tests not yet moved over from test_c_parser.py.
 - Rename foo to sample and add a test that parses this complete file.
 - Add global variable counting.
- Try it on some other code.
- Run it on a single file or on a folder?
- Make the output cleaner.