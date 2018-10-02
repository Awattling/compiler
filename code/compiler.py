#!/usr/bin/python

import sys
from pprint import pprint
import lexar
import parseryacc
import semanticAnalysis
import codeGen
#### Functions ####

## Recursive tree printing to file method ##
def prettyPrintToFile(root, offset, f, fname):
	if f is None:
		f = open(fname, 'w')
	for x in range(0,offset) :
		f.write("|")
		
	f.write(root.name)
	f.write('( ' + ' '.join(map(str,root.attributes)) + ' )')
	f.write('\n')
		
	for child in root.children:
		prettyPrintToFile(child, offset + 1, f, "NONE")

## Method to print Symbol Table to File ##
def printTableToFile(table, fname ):
	f = open(fname, 'w')
	for st in table:
		f.write('[' + st.name + ', ' +  st.scopeType + ', ' +st.returnType +  ', #variables:' + str(st.numberOfLocal) +   ', #arguments: ' + str(st.numberOfArguments) + ', #scope:' + str(st.scope))
		f.write ('\n')
		for attr in st.table:
			f.write("	   " + str( attr))
			f.write ('\n')
		f.write ("]")
		f.write ('\n')
		
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
			global lalrTracking
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
global lalrTracking
lalrTracking = False


argumentChecks()
file = openFile()

## Runs Lexing and Parsing with Lex and Yacc modules
# Returns an Abstract Syntax tree for semantic analysis
ast = parseryacc.parse(file.read(), lalrTracking)

##Ast output to file
prettyPrintToFile(ast, 0, None, "../logs/ast.txt")
print ("Check logs for Abstract Syntax Tree (ast.txt)")

## Semantic Analysis of AST ##
# Returns an Intermediate representation (IR) of the code and Symbol Table (ST)
(IR, ST) = semanticAnalysis.semanticAnalysis(ast)

## Output of IR to file
prettyPrintToFile(IR, 0, None, "../logs/IR.txt")
print ("Check logs for Itermediate Tree (IR.txt)")

## Output of Symbol Table to file ##
printTableToFile(ST, "../logs/ST.txt")
print ("Check logs for Symbol Table (ST.txt)")

## Code generation and output to file ##
code = codeGen.codeGen(IR)
fname = sys.argv[1].rsplit(".", 1)[0]
fname = fname + ".am"
outputfile = open(fname, 'w')
for item in code:
	outputfile.write(item + '\n')
	
print("Am stack code found in", fname)
