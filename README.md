# Daniel-Preconfig, a simple python-based config file generator

# SYNOPSIS

Daniel-Preconfig generates files from a template by evaluating double-bracketed Python code.
It has no dependencies other than python itself and is Free and Opensource

# DESCRIPTION

Daniel-Preconfig reads the template file from top to bottom, identifying snippets
of code which are surrounded by double square brackets. It then executes this
code using the python interpreter. If the square brackets start with an equals, the expression's value is
converted to their string representation, and substituted in place of the code snippet.
Otherwise, the code is simply 'exec(...)'ed.
Importantly, any accompanying text in the template file is copied verbatim to the output file,
such that any syntax present in the configuration file can be maintained during the process.

This allows for the generation of different config files based on one "main" template.
By adding python code that reads environment variables to the template, you can maintain
multiple config files while keeping the duplicated data in the same file and only
having to seperate the differences.

i.e. you can make a main template "config.template" and then

	VAR=a preconfig config.template config.a
	VAR=b preconfig config.template config.b

to make the a and b versions of the config.

This program was created based on Preconfig because I had a need for a configuration
file generator, and quite liked the double-bracket python syntax, but I had no need
for the generation of every possible combination of values. In fact, such capabilities
stopped the usage of the program that I needed. This is why I made a modified version that
only allowed creation of a single file at a time based on the variable definition specified.
It also changes the syntax of the double brackets to allow for blocks that do not evaluate to anything
and implements some indent-correction to allow for multi-line statements and expression.

Only one template and one output can be specified at a time.
# SYNTAX

preconfig [OPTIONS] TEMPLATE_FILE OUTPUT_FILE

# OPTIONS

if '--help' is specified, this documentation will be printed.

# CODE SNIPPETS

Code snippets can either be [[ ... ]] which will be 'exec'ed as python code but removed from the output file.
Indents will be corrected so the indent on the first line of the snippet will be removed from every subsequent line.
This keeps the python parser happy, which wants code to start with no indents while still allowing for indents for formatting.
Code snippets like [[= ... ]] will be 'eval'ed as python code and the string representation of the output will be
inserted into the output file with the snippet removed.

## Acknowledgments:

I would like to thank [Oliver Lugg](https://oliverlugg.bandcamp.com/) for his amazing music
and to my amazing girlfriend for supporting me more than I could ever ask for.

The original acknowledgments is kept below.

We wish to thank the members of the Nedelec group, and all users of Cytosim
for their feedback which has contributed greatly to this development.
We thanks Shaun Jackman and Steven Andrews for valuable feedback!

Copyright Daniel H. Karagory 2021

Copyright Francois J. Nedelec and Serge Dmitrieff

EMBL 2010--2017; Cambridge University 2019--2020

This is Free Software with no WARANTY, just hoping to be useful.

Preconfig is distributed under GPL3.0 Licence (see LICENCE)
