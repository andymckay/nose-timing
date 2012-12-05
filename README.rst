A simple plugin that combines test times and test setup times and writes the
output to JSON files. I ripped most of this out of nose-congestion:

https://github.com/acdha/nose-congestion

And added in a few bits for my own needs.

This is a work in progress to do what I want and not much more at this point.

Usage
-----

To install::

        pip install nose-timing

When running your tests add::

        --with-timing

To get your timing to run. By default it will write to your current directory
two files, `setup.json` and `tests.json`. To alter where it writes to::

        --output-directory=/tmp
