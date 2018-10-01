# compiler

Notes: 
Written in Python 3 (PLY's) Using Lex/Yacc module 
	- Copyright (C) 2001-2018 David M. Beazley (Dabeaz LLC) All rights reserved.
	- https://github.com/dabeaz/ply 

Usage: 
python compiler.py [testfilename] [optional T]

The optional T is for a tracking debug mode that displays what is happening within the LALR (Look ahead left to right) automation. 

#About

Lexical Analysis: 
- Lexical Analysis also known as "tokinizing" is the first stage of a compiler and generally serves to divide the input text into useful tokens.
- Here were using PLY's lex tool to divide things into tokens using regular expression matching. 
- "t_" within the code notates a token pattern (ie Regular Expression). 
- The lexar included also removes unimportant things like whitespaces and comments again using regular expressions. 
- http://www.dalkescientific.com/writings/NBN/parsing_with_ply.html is a great resource to learn more about using the PLY Lex and Yacc modules. 

Syntactical Analysis: 
- 