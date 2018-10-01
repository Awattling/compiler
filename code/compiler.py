#!/usr/bin/python

import sys
from pprint import pprint
import lexar
import parseryacc
import semanticAnalysis
import codeGen

#### Functions ####
def prettyPrint(root, offset, f, fname):
	if f is None:
		f = open(fname, 'w')

	
	for x in range(0,offset) :
		f.write("|")
		
	f.write(root.name)
	f.write('( ' + ' '.join(map(str,root.attributes)) + ' )')
	f.write('\n')
		
	for child in root.children:
		prettyPrint(child, offset + 1, f, "NONE")



def compile(filename):

	
	try:
		### Input handling, Lexing and Parsing
		if(len(sys.argv) == 3):
			if(sys.argv[2] == "T"):
				file = open(filename)
				ast = parseryacc.debugParse(file.read())
			else:
				print("Undefined input: " + sys.argv[2])
				print("Usage:") 
				print("compiler.py filename")
				print ("or")
				print("compiler.py filename T")
				print("NOTHING COMPILED")
				sys.exit()
		if(len(sys.argv) < 1 or len(sys.argv) > 3):
			print("Undefined input: " + sys.argv[2])
			print("Usage:") 
			print("compiler.py filename")
			print ("or")
			print("compiler.py filename T")
			print("NOTHING COMPILED")
			sys.exit()
		if(len(sys.argv) == 2):
			file = open(filename)
			ast = parseryacc.parse(file.read())
		
		##Ast output to file
		prettyPrint(ast, 0, None, "ast.txt")
		
		## Semantic Analysis of AST ##
		IR = semanticAnalysis.semanticAnalysis(ast)
		
		## Output of IR to file
		prettyPrint(IR, 0, None, "IR.txt")
		
		## Code generation and output to file ##
		code = codeGen.codeGen(IR)
		fname = filename.split(".")[0]
		outputfile = open(fname + ".am", 'w')
		for item in code:
			outputfile.write(item + '\n')
			
	except EOFError:
		print("Could not open file: " + filename )
		print("NOTHING COMPILED")
	
#### CODE ####
if len(sys.argv) < 2:
	print("Usage:") 
	print("compiler.py filename")
	print ("or")
	print("compiler.py filename T")
	sys.exit()
	
else:
	filename = sys.argv[1]
	compile(filename)
	
	
	

