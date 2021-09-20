# DANIEL-PRECONFIG, a (less) versatile configuation file generator

# Copyright Daniel H. Karagory, 2021
# this program is based on https://github.com/nedelec/preconfig and is modified to better meet my needs
# I am allowed to change this under the GPL V3 licesnse it was distributed with and it will continue to be distributed under that same licesnse
# I have left the original copyright notice below

# Copyright Francois J. Nedelec, EMBL 2010--2017, Cambridge University 2019--2020

"""
# Daniel_Preconfig, a simple python-based config file generator

# SYNOPSIS

Daniel-Preconfig generates files from a template by evaluating double-bracketed Python code.
It has no dependencies other than python itself and is Free and Opensource

# DESCRIPTION

Daniel_Preconfig reads the template file from top to bottom, identifying snippets
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

daniel-preconfig [OPTIONS] TEMPLATE_FILE OUTPUT_FILE

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
"""

import sys

try:
	import os, io, re
	GLOBALS = { 'random': __import__('random'), 'math': __import__('math') }
except ImportError:
	sys.stderr.write("Error: Preconfig could not load necessary python modules\n")
	sys.exit()

#-------------------------------------------------------------------------------

__VERSION__="2.1"

__DATE__   ="20.9.2021"

# code snippets are surrounded by double square brackets:
CODE = '['
DECO = ']'


# A function to return version to be able to pip package it
def version():
	return __VERSION__


#-------------------------------------------------------------------------------


def get_block(file, S, E):
	"""
	Extract from `file` the next block starting with DOUBLE delimiters 'SS'
		and ending with matching 'EE'.
	Returns 3 values:
		- the text found before the block start
		- the block with its delimiters
		- a boolean EOF indicator
	"""
	ch = file.read(1)
	sec = 0
	pre = ''
	blk = ''
	lev = 0
	while file and ch:
		pc = ch
		ch = file.read(1)
		if ch == S:
			if sec:
				lev += 1
			if pc == S:
				sec += 1
		if sec:
			blk += pc
			#print("%c%c >  lev %i sec %i" %(pc, ch, lev, sec))
		else:
			pre += pc
		if ch == E:
			if sec:
				lev -= 1
			if pc == E:
				#print("%c%c EE lev %i sec %i" %(pc, ch, lev, sec))
				if lev == -2:
					return (pre, blk+ch, False)
	# reaching end of file:
	return (pre, blk, True)


#-------------------------------------------------------------------------------
def evaluate(arg):
	"""
		Evaluate `arg` and return result
	"""
	res = arg
	#print("   evaluate("+arg+")")
	try:
		res = eval(arg, GLOBALS)
	except Exception as e:
		sys.stderr.write("\033[95m")
		sys.stderr.write("Error evaluating '%s'")
		sys.stderr.write("\033[0m")
		sys.stderr.write("	"+str(e)+'\n')
		sys.exit(1)
	if not isinstance(res, str):
		try:
			res = list(res)
		except Exception:
			pass
	#print("evaluate("+arg+") = " + repr(res))
	return res

def fixIndents(text):
	if text[0] == "\n":
		text = text[1:]
	
	indentPrefix = "\n"
	for c in text:
		if c == " " or c == "\t":
			indentPrefix += c
		else:
			break
	
	text = "\n" + text;
	text = text.replace(indentPrefix, "\n").strip()
	
	return text

def process(file, output):
	"""
		`process()` will identify and substitute bracketed code blocks
		embedded in the input file, and generate a file at EOF.
	"""
	text = ""

	while file:
		(pre, block, eof) = get_block(file, CODE, DECO)
		#print("%i characters +  '%s'" % (len(pre), block))
		text += pre
		if eof:
			if block:
				sys.stderr.write("Error: unclosed bracketted block in:\n");
				sys.stderr.write("	"+block.split('\n', 1)[0]+'\n');
				sys.exit(1)
			# having exhausted the input, we generate a file:
			make_file(output, text)
			return
		# remove outer brackets:
		val = block[2:-2]
		if val[0] == "=":
			val = val[1:]
			val = fixIndents(val)
			print("evaluating:\n[[=%s]]\n" % val)
			text += eval(val, GLOBALS)
		else:
			val = fixIndents(val)
			print("executing\n[[%s]]\n" % val)
			exec(val, GLOBALS)
		

def make_file(output, text):
	"""
	Create a file with the specified text
	"""
	#make directory if name includes a non-existent directory:
	dir = os.path.dirname(output)
	if dir and not os.path.isdir(dir):
		os.mkdir(dir)
	with open(output, 'w') as f:
		f.write(text)

def process_preconfig(input, output):
	"""
		process one file, input, and write to the output path
	"""
	
	with open(input, 'r') as file:
		process(file, output)

