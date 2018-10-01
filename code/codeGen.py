import sys
import os
from Node import Node 
from symbolTable import symbolTable
from pprint import pprint

labelnum = 1

def codeGen (IR):
	print("CODE GENERATION COMPLETE")
	code = []
	g_prog(IR, code)
	
	print("___________STACK CODE ____________")
	for item in code:
		print (item)
		
	return code
		

	
def g_prog(node, code):
	if node.name == "IPROG":
		code.append("LOAD_R %sp") #access pointer
		code.append("LOAD_R %sp") #set frame pointer from prog
		code.append("STORE_R %fp")
		code.append("ALLOC " + str(node.attributes[0]))
		for child in node.children:
			if child.name != "IFUN":
				g_stmt(child, code)
		code.append("ALLOC " + str(- node.attributes[0] - 1))
		code.append("HALT")
		for child in node.children:
			if child.name == "IFUN":
				g_fun(child, code)
	else:
		print("Something went wrong with the program")
		sys.exit(0)

def g_stmt(node, code):
	name = node.name
	if name == "IASS":
		g_IASS(node,code)
	elif name == "IWHILE":
		g_IWHILE(node, code)
	elif name == "ICOND":
		g_cond(node, code)
	elif name == "iREAD_I":
		g_readI(node, code)
	elif name == "iREAD_B":
		g_readB(node, code)
	elif name == "IPRINT":
		g_print(node, code)
	elif name == "iRETURN":
		g_return(node, code)
	elif name == "iBlock":
		g_iBlock(node,code)
	else:
		print(node.name)
		print("something went wrong with the statments")
		sys.exit();
		
def g_iBlock(node, code):
	code.append("LOAD_R %fp")
	code.append("ALLOC 1")
	code.append("LOAD_R %sp")
	code.append("STORE_R %fp")
	code.append("ALLOC " + str(node.attributes[0]))
	code.append("LOAD_I " + str(node.attributes[0] + 2))
	for child in node.children:
		if child.name == "IFUN":
			g_fun(child, code)
		else:
			g_stmt(child, code)
	code.append("LOAD_R %fp")
	code.append("LOAD_O " + str(node.attributes[0] + 1))
	code.append("APP NEG")
	code.append("ALLOC_S")
	code.append("STORE_R %fp")
	
	
	
def g_IWHILE(node, code):
	global labelnum
	code.append("JUMP label" + str(labelnum+1))
	code.append("label"+ str(labelnum) + ": LOAD_R %fp")
	labelnum += 1
	#for child in node.children:
		#if child.name != "IAPP":
			#print(child.name)
	g_stmt(node.children[1], code)
	code.append("label" + str(labelnum) + ": LOAD_R %fp")	
	labelnum += 1
	g_expr(node.children[0], code)
	code.append("APP NOT")
	code.append("JUMP_C label" + str(labelnum - 2))
	
	
	
def g_return(node, code):
	g_expr(node.children[0], code)
	
def g_IASS (node, code):
	g_expr(node.children[0], code)
	code.append("LOAD_R %fp")
	code.append("STORE_O " + str(node.attributes[1]))
	
def g_cond(node, code):
	global labelnum
	g_expr(node.children[0], code)
	code.append("JUMP_C label" + str(labelnum))
	g_stmt(node.children[1],code)
	code.append("JUMP label" + str(labelnum + 1))
	code.append("label"+ str(labelnum) + ": LOAD_R %fp")
	labelnum += 1
	g_stmt(node.children[2],code)
	code.append("label"+ str(labelnum) + ": LOAD_R %fp")
	labelnum += 1
		
def g_readI(node, code):
	code.append("READ_I")
	code.append("LOAD_R %fp")
	code.append("STORE_O " + str(node.attributes[1]))
	
def g_readB(node, code):
	code.append("READ_B")
	code.append("LOAD_R %fp")
	code.append("STORE_O " + str(node.attributes[1]))
	
def g_print(node, code):
	g_expr(node.children[0], code)
	if(node.attributes[0] == "M_int"):
		code.append("PRINT_I")
	elif(node.attributes[0] == "M_bool"):
		code.append("PRINT_B")
	else:
		print("TYPE CONFLIT TTHITFDS")
	
def g_fun(node, code):
	code.append("fun_" + node.attributes[0] + ": LOAD_R %sp")
	code.append("STORE_R %fp")
	code.append("ALLOC " + str(node.attributes[1]))
	code.append("LOAD_I "+ str(node.attributes[1] + 3))
	for child in node.children:
		g_stmt(child, code)
	
	code.append("LOAD_R %fp")
	code.append("STORE_O " + str(- (node.attributes[2] + 3)))
	code.append("LOAD_R %fp")
	
	code.append("LOAD_O 0")
	code.append("LOAD_R %fp")
	code.append("STORE_O " + str(- (node.attributes[2] + 2)))
	
	code.append("LOAD_R %fp")
	code.append("LOAD_O " + str(node.attributes[1] + 1))
	code.append("APP NEG")
	code.append("ALLOC_S")
	code.append("STORE_R %fp")
	
	code.append("ALLOC " + str(-node.attributes[2]))
	code.append("JUMP_S")

	
def g_expr(node, code):
	if node.name == "INUM":
		g_INUM(node, code)
	elif node.name == "IBOOL":
		g_IBOOL(node, code)
	elif node.name == "IID":
		g_IID(node, code)
	elif node.name == "IAPP":
		g_opn(node.children[0], code)
	else:
		g_opn(node, code)
		
def g_IBOOL(node, code):
	code.append("LOAD_B " +  node.attributes[0])

def g_IID(node, code):
	if(node.attributes[2] == 1):
		code.append("LOAD_R %fp")
		code.append("LOAD_O " + str(node.attributes[1]))
	else:
		code.append("LOAD_O -2")
		code.append("LOAD_O " + str(node.attributes[1]))
		
def g_INUM(node, code):
	code.append("LOAD_I " + str(node.attributes[0]))
	
def g_opn(node,code):
	name = node.name
	if name == "ICALL":
		g_ICALL(node, code)
	elif name == "IMUL":
		forexpr(node,code)
		code.append("APP MUL")
	elif name == "ISUB":
		forexpr(node,code)
		code.append("APP SUB")
	elif name == "IADD":
		forexpr(node,code)
		code.append("APP ADD")
	elif name == "IDIV":
		forexpr(node,code)
		code.append("APP DIV")	
	elif name == "INEG":
		g_NEG(node, code)
	elif name == "ILT":
		forexpr(node,code)
		code.append("APP LT")
	elif name == "ILE":
		forexpr(node,code)
		code.append("APP LE")
	elif name == "IGT":
		forexpr(node,code)
		code.append("APP GT")
	elif name == "IGE":
		forexpr(node,code)
		code.append("APP GE")
	elif name == "IEQ":
		forexpr(node,code)
		code.append("APP EQ")
	elif name == "INOT":
		forexpr(node,code)
		code.append("APP NOT")
	elif name == "IAND":
		forexpr(node,code)
		code.append("APP AND")
	elif name == "IOR":
		forexpr(node,code)
		code.append("APP OR")
	else:
		print(name + " FATAL ERROR")
		sys.exit()

		
def forexpr(node, code):
	for child in node.children:
		g_expr(child, code)

	
def g_ICALL(node, code):	
	for child in node.children:
		g_expr(child, code)
	code.append("ALLOC 1")
	code.append("LOAD_R %fp")
	code.append("LOAD_R %fp")
	code.append("LOAD_R %cp")
	code.append("JUMP fun_" + node.attributes[0])
	

	
	
