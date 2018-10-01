import ply.lex
import sys

line = 0
# Word Tokens
reserved = {
	'not' : 'NOT',
	'if' : 'IF',
	#'of' : 'OF',
	'then' : 'THEN', 
	'while' : 'WHILE',
	'do' : 'DO',
	'read': 'READ',
	'else' : 'ELSE',
	'begin' : 'BEGIN',
	'end' : 'END',
	'print' : 'PRINT',
	'int' : 'INT',
	'bool' : 'BOOL',
	#'char' : 'CHAR',
	#'real' : 'REAL',
	'var' : 'VAR',
	#'size' : 'SIZE',
	#'float' : 'FLOAT',
	#'floor' : 'FLOOR',
	#'ceil' : 'CEIL',
	'fun' : 'FUN',
	'return' : 'RETURN',
	'true' : 'BVAL',
	'false' : 'BVAL',
	#'data'  : 'DATA',
	#'case'  : 'CASE',
}

# Other Tokens 
tokens = [ 
'ID',
#'IVAL',
#'RVAL',
'ADD',
'SUB',
'MUL',
'DIV',
#'ARROW',
'AND',
'OR',
'EQUAL',
'LT',
'GT',
'LE',
'GE',
'ASSIGN',
'LPAR',
'RPAR',
'CLPAR',
'CRPAR',
#'SLPAR',
#'SRPAR',
#'SLASH',
'COLON',
'SEMICOLON',
'COMMA',
'NUM',
#'CID',
'COMMENT',
'COMMENTM',
] + list(reserved.values())


# Rules for simple tokens
t_COLON	=	r':'
t_ASSIGN	= r':='
t_ADD 		= r'\+'
t_SUB 		= r'-'
t_MUL		= r'\*'
t_DIV		= r'/'
#t_SLASH 	= r'\|'
#t_ARROW 	= r'=>'
t_AND 		= r'&&'
t_OR		= r'\|\|'
t_EQUAL 	= r'='
t_LT		= r'<'
t_GT		= r'>'
t_LE		= r'=<'
t_GE		= r'>='
t_COMMA		= r'\,'
t_LPAR		= r'\('
t_RPAR		= r'\)'
t_CLPAR		= r'\{'
t_CRPAR		= r'\}'
#t_SLPAR		= r'\['
#t_SRPAR		= r'\]'

t_SEMICOLON = r'\;'

## Ignores Spaces
t_ignore	= r' '


# Rules for more complicated items. 
def t_ignore_COMMENT(t):
	r'\%.*'

def t_ignore_COMMENTM(t):
	r'(/\*(.|\n)*?\*/)|(//.*)'
	
# counts line Number 
def t_newline(t): 
	r'\n+' 
	t.lexer.lineno += t.value.count("\n")

def t_RVAL(t):
	r'-?\d+\.\d*(e-?\d+)?'
	#r'\f+'
	#r'[0-9]*.[0-9]+'
	return t
	
def t_NUM(t):
	r'\d+'
	return t

# Note this is the gate to all the "word Tokens"
def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved:
		t.type = reserved[t.value]
	return t	

# Handles unknown symbols 
def t_error(t):
	print ("Error: unrecognized character '%s'" % t.value[0])
	t.lexer.skip(1)
	sys.exit()
	
	
	
## Lexar is built when the file is imported ##
ply.lex.lex()


## Lexing function ##
def lex(strList):

	tokens = []
	i = 0

	while (i < len(strList)):
		cur = strList[i]
		if(cur == ''):
			i = i + 1
			continue
		ply.lex.input(cur)
		tok = ply.lex.token()
		#cur = cur[len(tok.value):]
		strList[i] = cur
		
		if(strList[i] == ''):
			i = i + 1
			
		tokens.append(tok)
		
	
	print("Lexing Complete")
		