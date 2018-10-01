#!/usr/bin/python

import sys
from pprint import pprint
import lexar
import parseryacc
import semanticAnalysis
import codeGen

#### Functions ####
def prettyPrintToFile(root, offset, f, fname):
	if f is None:
		f = open(fname, 'w')
	for x in range(0,offset) :
		f.write("|")
		
	f.write(root.name)
	f.write('( ' + ' '.join(map(str,root.attributes)) + ' )')
	f.write('\n')
		
	for child in root.children:
		prettyPrint(child, offset + 1, f, "NONE")

## Incorrect Usage error message ##	
def incorrectUsage():
	print("Usage:") 
	print("compiler.py filename")
	print("or")
	print("compiler.py filename T")
	print("NOTHING COMPILED")
	sys.exit()

## Checking command line Arguments ##
def argumentChecks():
	## If number of cmd arguments does not correspond to any options ##
	if(len(sys.argv) < 2 or len(sys.argv) > 3):
		incorrectUsage()
	elif(len(sys.argv) == 3):
	## if the second argument does not correspond ##
		if(sys.argv[2] != "T"):
			incorrectUsage()
		else:
			lalrTracking = True

## Attempting to open file for compilation ##
def openFile():
	try:
		file = open(sys.argv[1])
		return file
	except IOError:
		print("Error opening file for compilation")
		print("Please check to make sure the filename and location are correct")
		sys.exit()

#### MAIN RUNNING CODE ####
lalrTracking = False
argumentChecks()
file = openFile()

## Runs Lexing and Parsing with Lex and Yacc modules
ast = parseryacc.parse(file.read())

##Ast output to file
#prettyPrintToFile(ast, 0, None, "ast.txt")

## Semantic Analysis of AST ##
#IR = semanticAnalysis.semanticAnalysis(ast)

## Output of IR to file
#prettyPrint(IR, 0, None, "IR.txt")

## Code generation and output to file ##
#code = codeGen.codeGen(IR)
#fname = filename.split(".")[0]
#outputfile = open(fname + ".am", 'w')
#for item in code:
#	outputfile.write(item + '\n')



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

## Incorrect Usage error message ##	
def incorrectUsage():
	print("Usage:") 
	print("compiler.py filename")
	print("or")
	print("compiler.py filename T")
	print("NOTHING COMPILED")
	sys.exit()

## Checking command line Arguments ##
def argumentChecks():
	## If number of cmd arguments does not correspond to any options ##
	if(len(sys.argv) < 2 or len(sys.argv) > 3):
		incorrectUsage()
	elif(len(sys.argv) == 3):
	## if the second argument does not correspond ##
		if(sys.argv[2] != "T"):
			incorrectUsage()
		else:
			lalrTracking = True

## Attempting to open file for compilation ##
def openFile():
	try:
		file = open(sys.argv[1])
		return file
	except IOError:
		print("Error opening file for compilation")
		print("Please check to make sure the filename and location are correct")
		sys.exit()
		

