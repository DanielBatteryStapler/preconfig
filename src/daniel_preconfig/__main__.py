from . import preconfig
import sys

def handle_arguments(args):
	"""
		process arguments and perform corresponding task
	"""
	
	input = ""
	output = ""
	
	for arg in args:
		if input == "":
			input = arg
		elif output == "":
			output = arg
		else:
			sys.stderr.write("  Error: too many arguments\n")
			sys.exit()
	

	if input == "":
		sys.stderr.write("  Error: you must specify an input template file\n")
		sys.exit()
   	
	if output == "":
		sys.stderr.write("  Error: you must specify an output template file\n")
		sys.exit()
	
	process_preconfig(input, output)

def main():
	if len(sys.argv) < 2:
		print("You must specify a template file (for instructions, invoke with option '--help')")
	elif sys.argv[1].endswith("help"):
		print(__doc__)
	elif sys.argv[1]=='--version':
		print("This is PRECONFIG version %s (%s)" %(__VERSION__,__DATE__))
	else:
		handle_arguments(sys.argv[1:])

if __name__ == '__main__':
	main()
