import sys
import os
from Node import Node 
from symbolTable import symbolTable
from pprint import pprint

ST = []	

def semanticAnalysis (ast):
	STtableCreation(ST, ast, 0)
	IR = wf_I_prog(ast)
	print("SEMANTIC ANALYSIS COMPLETE")
	#prettyPrint(IR,0)
	printTable(ST)
	printfix(IR)
	
	return IR
	
def printfix(node):
	for child in node.children:
		if child.name == "IPRINT":
			child.addAttribute(printfixhelper(child))
			printfixhelper(child)
		printfix(child)

def printfixhelper(node):
	
	name = node.children[0].name
	if name == "IID":
		item = lookup(node.children[0].attributes[0], 100)
		(type, varname, varType, offset, scopefound) = item
		return varType
	elif name == "INUM" or "IADD" or "IMUL" or "ISUB" or "IDIV" or "INEG":
		return"M_int"
	elif name == "IBOOL" or "ILT" or "ILE" or "IGT" or "IGE" or "IEQ" or "INOT" or "IAND" or "IOR":
		return "M_bool"
	elif name == "IAPP":
		return printfixhelper(node.children[0])
	elif name == "ICALL":
		item = lookup(node.children[0].attributes[0], 100, )
		(NA, varname, arguments, returnType, offset, scopefound) = item
		return returnType
	else:
		print("AHAHAHAH TYPE")
		
def wf_I_prog(node):
	if node.name == "M_prog":
		newNode = Node("IPROG")
		table = getTable("Prog")
		newNode.addAttribute(table.numberOfLocal)
		
		for child in node.children:
			if(child.name == "M_fun"):
				newNode.addChild(wf_I_fbody(child, 0))
		for child in node.children:
			if(child.name != "M_var" and child.name != "M_fun"):
				newNode.addChild(wf_I_stmt(child, 0))
		return newNode
		
	
def wf_I_fbody(current, scope):
	for child in current.children:
		
		if child.name == "M_block":
			scope = scope + 1
			newNode = Node("IFUN")
			table = getTable(current.attributes[0])
			if(table == None):
				print("function " + current.attributes[0] + " not defined in current scope")
				sys.exit()
				
			newNode.addAttribute(current.attributes[0])
			newNode.addAttribute(table.numberOfLocal)
			newNode.addAttribute(table.numberOfArguments)
					
			for tiny in child.children:
				if(tiny.name == "M_return"):
					newNode.addChild(wf_iRETURN(tiny, current.attributes[0], scope))
				elif(tiny.name == "M_fun"):
					newNode.addChild(wf_I_fbody(tiny, scope))
				elif(tiny.name != "M_var" and tiny.name != "M_fun"):
					newNode.addChild(wf_I_stmt(tiny, scope))
	return newNode
	
def wf_iRETURN(node, name, scope):
	item = lookup(name, scope)
	if item == None:
		print("Something wrong with return statements")
		sys.exit()
	else:
		newNode = Node("iRETURN")
		(type, varname, arguments, returnType, offset, scopefound) = item
		if(returnType == "M_int"):
			newNode.addChild(wf_I_expr(node.children[0], "Int", scope))
		elif(returnType == "M_bool"):
			newNode.addChild(wf_I_expr(node.children[0], "Bool", scope))
		else:
			print("Unsupported return type: " + returnType)
			sys.exit()
		return newNode
	
def wf_I_stmt(current, scope):
	name = current.name
	if name == "M_ass":
		return wf_IASS(current, scope)
	elif name == "M_while":
		return wf_IWHILE(current, scope)
	elif name == "M_cond":
		return wf_ICOND(current, scope)
	elif name == "M_read":
		return wf_read(current, scope)
	elif name == "M_print":
		return wf_print(current, scope)
	elif name == "M_block":
		return wf_iBLOCK(current, scope)
	else:
		print("Incorrect statement: " + name)
		sys.exit()
	
def wf_IASS (node, scope):
	newNode = Node("IASS")
	item = lookup(node.attributes[0], scope)
	if(item == None):
		print("Variable " + node.attributes[0] + " not found for assignment")
		sys.exit()
	else:
		(type, varname, varType, offset, scopefound) = item
		newNode.addAttribute(node.attributes[0])
		newNode.addAttribute(offset)
		if(varType == "M_int"):
			newNode.addChild(wf_I_expr(node.children[0], "Int", scope))
		elif(varType == "M_bool"):
			newNode.addChild(wf_I_expr(node.children[0],"Bool", scope))
	return newNode
			
def wf_IWHILE(node, scope):
	newNode = Node("IWHILE")
	newNode.addChild(wf_I_expr(node.children[0], "Bool", scope))
	newNode.addChild(wf_I_stmt(node.children[1], scope))
	return newNode
	
def wf_ICOND(node, scope):
	newNode = Node("ICOND")
	newNode.addChild(wf_I_expr(node.children[0], "Bool", scope))
	newNode.addChild(wf_I_stmt(node.children[1], scope))
	newNode.addChild(wf_I_stmt(node.children[2], scope))
	return newNode
	
def wf_read(current, scope):
	item = lookup(current.attributes[0], scope)
	if(item == None):
		print ("variable " + current.attributes[0] + " not found in this scope")
		sys.exit()
	else:
		(type, varname, varType, offset, scopefound) = item
		
		if (varType == "M_int"):
			newNode = Node("iREAD_I")
			newNode.addAttribute(current.attributes[0])
			newNode.addAttribute(offset)
			return newNode
		elif(varType == "M_bool"):
			newNode = Node("iREAD_B")
			newNode.addAttribute(current.attributes[0])
			newNode.addAttribute(offset)
			return newNode
		
def wf_print(current, scope):
	newNode = Node("IPRINT")
	newNode.addChild(wf_I_expr(current.children[0], "Print", scope))
	return newNode
	
	
def wf_iBLOCK(node, scope):
	newNode = Node("iBlock")
	tally = 0
	for child in node.children:
		if child.name == "M_fun":
			newNode.addChild(wf_I_fbody(child, scope))
		elif child.name == "M_var":
			tally += 1
		else:
			newNode.addChild(wf_I_stmt(child, scope))
	newNode.addAttribute(tally)
	return newNode	
	
	
def wf_I_expr(node, type, scope):
	if(node.name == "M_num"):
		if type == "Int" or type == "Print":
			newNode = Node("INUM")
			newNode.addAttribute(int(node.attributes[0]))
			return newNode
		else:
			print("Incompatible types")
			sys.exit()	
	elif(node.name == "M_bl"):
		if type == "Bool" or type == "Print":
			newNode = Node("IBOOL")
			newNode.addAttribute(node.attributes[0])
			return newNode
		else:
			print("Incompatible types")
			sys.exit()
	elif(node.name == "M_id"):
		newNode = wf_IID(node, type, scope)
		return newNode
	else:
		return wf_I_APP(node, type, scope)
	
def wf_IID(node, type, scope):
	item = lookup(node.attributes[0], scope)
	
	
	if(item == None):
		print("ID " + node.attributes[0] + " not found in this scope")
		sys.exit()
	else:
		(STtype, varname, varType, offset, scopefound) = item
	
	if(scopefound != scope):
		scopefound = 0
	else:
		scopefound = 1
		
	if(varType == "M_int" and (type == "Int" or type == "Print")):
		newNode = Node("IID")
		newNode.addAttribute(node.attributes[0])
		newNode.addAttribute(offset)
		newNode.addAttribute(scopefound)
		return newNode	
	elif(varType == "M_bool" and (type == "Bool" or type == "Print")):
		newNode = Node("IID")
		newNode.addAttribute(node.attributes[0])
		newNode.addAttribute(offset)
		newNode.addAttribute(scopefound)
		return newNode	
	else:
		print("Variable " + node.attributes[0] +" not the required type of " + type)
		sys.exit()
	
	
def wf_I_APP(node, type, scope):
	newNode = Node("IAPP")
	if(node.name == "M_fn"):
		newNode.addChild( wf_ICALL(node, type, scope))
		return newNode
	elif(node.name == "M_app"):
		newNode.addChild(wf_I_opn(node.children[0], type, scope))
		return newNode
	else:
		newNode.addChild(wf_I_opn(node, type, scope))
		return newNode
		
def wf_I_opn(node, type, scope):
	if(node.name == "M_fn"):
		newNode = wf_ICALL(node, type, scope)
	elif(node.name == "M_app"):
		newNode = Node("IAPP")
		newNode.addChild(wf_I_opn(node.children[0], type, scope))
	elif(type == "Int"):
		newNode = wf_I_Int(node, scope)
	elif(type == "Bool"):
		newNode = wf_I_Bool(node, scope)
	else:
		print("incompatible type and expression")
		sys.exit()
	return newNode

def wf_I_Bool(node, scope):
	if(node.name == "M_eq"):
		newNode = Node("IEQ")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))
	elif(node.name == "M_ge"):
		newNode = Node("IGE")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))
	elif(node.name == "M_gt"):
		newNode = Node("IGT")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))	
	elif(node.name == "M_le"):
		newNode = Node("ILE")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))	
	elif(node.name == "M_lt"):
		newNode = Node("ILT")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))		
	elif(node.name == "M_and"):
		newNode = Node("IAND")
		for child in node.children:
			newNode.addChild(wf_I_opn(child, "Bool", scope))
	elif(node.name == "M_not" and type == "Bool"):
		newNode = Node("INOT")
		for child in node.children:
			newNode.addChild(wf_I_opn(child, "Bool", scope))
	elif(node.name == "M_or" and type == "Bool"):
		newNode = Node("IOR")
		for child in node.children:
			newNode.addChild(wf_I_opn(child, "Bool", scope))
	else:
		print("Expected boolean expression but got " + node.name+ " Instead") 
		sys.exit()
	return newNode
	
def wf_I_Int(node, scope):
	if(node.name == "M_mul"):
		newNode = Node("IMUL")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))
	elif(node.name == "M_add"):
		newNode = Node("IADD")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))
	elif(node.name == "M_sub"):
		newNode = Node("ISUB")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))
	elif(node.name == "M_div"):
		newNode = Node("IDIV")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))
	elif(node.name == "M_neg"):
		newNode = Node("INEG")
		for child in node.children:
			newNode.addChild(wf_I_expr(child, "Int", scope))
	else:
		print("Expected Integer expression but got " + node.name+ " Instead") 
		sys.exit()
	return newNode

	
def wf_ICALL(node, type, scope):
	newNode = Node("ICALL")
	newNode.addAttribute(node.attributes[0])
	item = lookup(node.attributes[0], scope)
	if item != None:
		(NA, varname, arguments, returnType, offset, scopefound) = item
	else:
		print("Function " + node.attributes[0] + " Not found")
		sys.exit()
	arguments = flatten(arguments)
	if 2 * (len(node.children)) == len(arguments):
		value = 1
		for child in node.children:
			if arguments[value] == "M_int":
				newNode.addChild(wf_I_expr(child, "Int", scope))
			elif(arguments[value] == "M_bool"):
				newNode.addChild(wf_I_expr(child, "Bool", scope))
			else:
				print("Invalid Argument Type")
				sys.exit()
			value += 2
		return newNode
	else:
		print("Improper number of arguments in function call")
	
	if(returnType == "M_int" and (type == "Int" or type == "Print")):
		return newNode
	elif(returnType == "M_bool" and (type == "Bool" or type == "Print")):
		return newNode
	else:
		print("Function call return type does not match type of calling code")
		sys.exit()

def getTable(name):
	global ST
	for table in ST:
		if table.name == name:
			return table
	

def lookup(name, scope):
	global ST
	while scope >= 0:
		for table in ST:
			if(table.scope == scope):
				item = table.lookuptable(name)
				if item != None:
					item2 = item + (scope,)
					return item2
		scope -= 1
	return None
	
def lookup2(name, scope):
	for table in ST:
		if(table.scope == scope):
			item = table.lookuptable(name)
			if item != None:
				return item
	
	
def STtableCreation (table, node, scope):
	name = node.name
	if name == "M_prog":
		newTable = symbolTable("L_PROG", "None", scope, "Prog")
		table.insert(0,newTable)
		for child in node.children:
			if(child.name == "M_var"):
				tuple = child.attributes[0]
				(name, type) = tuple
				newTable.addVarAttr("Var_attr", name, type)
			
			elif(child.name == "M_fun"):
				newTable.addAttr("Fun_attr", child.attributes[0], child.attributes[1], child.attributes[2], 0)
				STtableCreation(table, child, (scope + 1))

	if name == "M_fun":
		newTable = symbolTable("L_FUN", node.attributes[2], scope, node.attributes[0])
		tupleHandler(node.attributes[1], newTable)
		table.insert(0,newTable)
		
		for child in node.children:
			for block in child.children :
				if(block.name == "M_var"):
					tuple = block.attributes[0]
					(name, type) = tuple
					newTable.addVarAttr("Var_attr", name, type)
				
				elif(block.name == "M_fun"):
					newTable.addAttr("Fun_attr", block.attributes[0], block.attributes[1], block.attributes[2], 0)
					STtableCreation(table, block, scope + 1)

def tupleHandler(tuple, table):
	flat = flatten(tuple)
	indexed = list(flat)
	i = 0
	while i < len(indexed):
		name = indexed[i] 
		type = indexed[i + 1]
		table.addArgAttr("Var_attr", name, type)
		i += 2
		
def flatten(T):
	if not isinstance(T, tuple):
		return (T,)
	elif len(T) == 0: 
		return ()
	else:
		return flatten(T[0]) + flatten(T[1:])
					
def printTable(current):
	for st in current:
		print('[' + st.name + ', ' +  st.scopeType + ', ' +st.returnType +  ', #variables:' + str(st.numberOfLocal) +   ', #arguments: ' + str(st.numberOfArguments) + ', #scope:' + str(st.scope))
		for attr in st.table:
			print("	   " + str( attr))
		print ("]")
		
def prettyPrint(current, offset):
	x = 0
	while x < offset:
		print("|", end = "")
		x += 1
	print(current.name + " " + str(current.attributes))
	for child in current.children:
		prettyPrint(child, (offset + 1))