import sys
import ply.yacc
import lexar
from Node import Node 

tokens = lexar.tokens

def p_prog(p):
	'''prog : block'''	
	p[0] = Node("M_prog")
	p[0].addChildren(p[1])
	
def p_block(p):
	'''block : declarations program_body'''
	p[0] = p[1], p[2]

	
def p_declarations(p):
	'''declarations : declaration SEMICOLON declarations
					|  '''
	
	if len(p) > 1:
		if p[3] is not None:
			p[0] = p[1] , p[3]
		else:
			p[0] = p[1]
	
def p_declaration(p):
	'''declaration : var_declaration
				   | fun_declaration'''
	p[0] = p[1]

def p_var_declaration(p):
	'''var_declaration : VAR basic_var_declaration'''
	p[0] = Node("M_var")
	p[0].addAttribute(p[2])

def p_basic_var_declaration(p):
	'''basic_var_declaration : identifier COLON type'''
	p[0] = (p[1], p[3])
	
	
def p_fun_declaration(p):
	'''fun_declaration : FUN identifier param_list COLON type CLPAR fun_block CRPAR'''
	p[0] = Node("M_fun")
	p[0].addAttribute(p[2])
	p[0].addAttribute(p[3])
	p[0].addAttribute(p[5])
	p[0].addChild(p[7])
	
def p_fun_block (p):
	'''fun_block : declarations fun_body'''
	p[0] = Node("M_block")
	if p[1] is not None:
		p[0].addChild(p[1])
	p[0].addChildren(p[2])
	
def p_param_list (p):
	'''param_list : LPAR parameters RPAR'''
	p[0] = p[2]
	
def p_parameters (p):
	'''parameters : parameters1
				  | '''
	if len(p) > 1:
		p[0] = p[1]
	
def p_parammeters1 (p):
	''' parameters1 : parameters1 COMMA basic_var_declaration
					| basic_var_declaration'''
				
	if len(p) > 2:
		p[0] = p[1], p[3]
	else:
		p[0] = p[1]
		
def p_identifier (p):
	'''identifier : ID'''
	p[0] = p[1]
	
def p_type (p):
	'''type : INT
			| BOOL'''

	if p[1] == "int":
		p[0] = 'M_int'
	elif p[1] == "bool":
		p[0] = 'M_bool'
	
	
	
def p_program_body(p):
	''' program_body : BEGIN prog_stmts END'''
	p[0] = p[2]

				  	
def p_fun_body (p):
	'''fun_body : BEGIN prog_stmts RETURN expr SEMICOLON END
				| prog_stmts RETURN expr SEMICOLON'''
	if len(p) == 7:
		ret = Node("M_return")
		ret.addChild(p[4])
		if p[2] is not None:
			p[0] = p[2] , ret
		else: 
			p[0] = ret
	else:
		ret = Node("M_return")
		ret.addChild(p[3])
		if p[1] is not None:
			p[0] = p[1] , ret
		else: 
			p[0] = ret
		
def p_prog_stmts (p):
	'''prog_stmts : prog_stmt SEMICOLON prog_stmts
				  | '''
	if len(p) > 1:
		if p[3] is not None:
			p[0] = p[1],p[3]
		else:
			p[0] = p[1]

def p_prog_stmt (p):
	'''prog_stmt : IF expr THEN prog_stmt ELSE prog_stmt 
				 | WHILE expr DO prog_stmt
				 | READ ID
				 | ID ASSIGN expr
				 | PRINT expr
				 | CLPAR block CRPAR'''
			
	if len(p) == 7:
		p[0] = Node('M_cond')
		p[0].addChild(p[2])
		p[0].addChild(p[4])
		p[0].addChild(p[6])
	elif len(p) == 5:
		p[0] = Node('M_while')
		p[0].addChild(p[2])
		p[0].addChild(p[4])
	elif len(p) == 4:
		if p[1] == '{':
			p[0] = Node('M_block')
			p[0].addChildren(p[2])
		else: 
			p[0] = Node('M_ass')
			p[0].addAttribute(p[1])
			p[0].addChild(p[3])
			
	elif len (p) == 3:
		if p[1] == "read":
			p[0] = Node('M_read')
			p[0].addAttribute(p[2])
		else:
			p[0] = Node('M_print')
			p[0].addChild(p[2])
				
	
def p_expr (p):
	''' expr : expr OR bint_term
			 | bint_term'''
	if len(p)> 2:
		p[0] = Node('M_or')
		p[0].addchild(p[1])
		p[0].addchild(p[3])
	else:
		p[0] = p[1]				   
					   
	
def p_bint_term (p):
	''' bint_term : bint_term AND bint_factor
				  | bint_factor'''
	if len(p)> 2:
		p[0] = Node('M_and')
		p[0].addChildren((p[1],p[3]))
	else:
		p[0] = p[1]
	
def p_bint_factor (p):
	'''bint_factor : NOT bint_factor
				   | int_expr compare_op int_expr
				   | int_expr'''

	
	if len(p)> 3:
		p[0] = Node("M_app")
		p[0].addChild(p[2])
		p[2].addChild(p[1])
		p[2].addChild(p[3])	
	elif len(p)> 2:
		p[0] = Node("M_not")
		p[0].addChild(p[2])
	else:
		p[0] = Node("M_app")
		p[0] = p[1]
				   	
def p_compare_op (p):
	'''compare_op : EQUAL
				  | LT
				  | GT
				  | LE
				  | GE'''
	if p[1] == "=":
		p[0] = Node('M_eq')
	elif [1] == "<":
		p[0] = Node('M_lt')
	elif p[1] == ">":
		p[0] = Node('M_gt')
	elif p[1] == "=<":
		p[0] = Node('M_le')
	elif p[1] == ">=":
		p[0] = Node('M_ge')


	

def p_int_expr (p):
	'''int_expr : int_expr addop int_term
				| int_term'''
	if len(p) > 2:
		p[0] = p[2]
		p[0].addChild(p[1])
		p[0].addChild(p[3])
	else:
		p[0] = p[1]
		
def p_addop (p):
	'''addop : ADD
			 | SUB'''
	if p[1] == "+":
		p[0] = Node('M_add')
	else:
		p[0] = Node('M_sub')
		
def p_int_term (p):
	'''int_term : int_term mulop int_factor
				| int_factor'''
	if len(p)> 2:
		p[0] = p[2]
		p[2].addChild(p[1])
		p[2].addChild(p[3])
	else:
		p[0] = p[1]	
		
		
def p_mulop (p):
	'''mulop : MUL
			 | DIV'''
	if p[1] == "*":
		p[0] = Node('M_mul')
	else:
		p[0] = Node('M_div')
	
		
def p_int_factor (p):
	'''int_factor : LPAR expr RPAR
				  | ID argument_list
				  | NUM
				  | BVAL
				  | SUB int_factor'''

	if len(p) == 4:	
		p[0] = p[2]
	if len(p) == 3:
		if(p[1] == "sub"):
			p[0] = Node('M_sub')
			p[0].addChild(p[2])
		else:
			p[0] = p[2]
			p[0].addAttribute(p[1])
			#p[0].addChild(p[2])
		#p[0].addChild(p[2])
	if len(p) == 2:
		if p[1] == "true":
			p[0] = Node('M_bl')
			p[0].addAttribute("TRUE")
		elif p[1] == "false":
			p[0] = Node('M_bl')
			p[0].addAttribute("FALSE")
		else:
			p[0] = Node('M_num')
			p[0].addAttribute(p[1])
				
def p_argument_list(p):
	'''argument_list : LPAR arguments RPAR
					 | '''
					 
	if len(p) > 1:
		p[0] = Node('M_fn')
		p[0].addChildren(p[2])		
	else:
		p[0] = Node("M_id")
		
def p_arguments (p):
	'''arguments : arguments1
				 | '''
	if len(p) > 1:
		p[0] = p[1]
		
def p_arguments1 (p):
	''' arguments1 : arguments1 COMMA expr
				   | expr '''
				   
	if len(p) > 2:
		p[0] = p[1],p[3]
	else:
		p[0] = p[1]
		
def p_error (p):
	print("ERROR: Parsing Error at line '%s' " %p.lineno, "Found '%s' " %p.value, "but expected something different")
	print(p)
	sys.exit()
	
	
# Building the parser #
ply.yacc.yacc()	



### CALL THIS ###
def parse(data, debug):
	ast = ply.yacc.parse(data, tracking = True, debug = debug)
	print("LEXING DONE")
	print("PARSING DONE")
	return ast;
	