class symbolTable(object):
	
	## Initilizing function symbol table ##	
	def __init__(self, scopeType, returnType, scope, name):
		self.name = name
		self.scopeType = scopeType #fun
		self.returnType = returnType
		self.numberOfLocal = 0
		self.numberOfArguments = 0
		self.scope = scope
		self.offset = 0
		self.argOffset = -3
		self.table = []
		
	
	
	# Adding variable to table
	def addVarAttr(self, type, name, varType):
		self.offset += 1
		self.table.append((type, name, varType, self.offset))
		self.numberOfLocal +=1
	
	# Adding Argument to table
	def addArgAttr(self, type, name, varType):
		self.argOffset -= 1
		self.table.append((type, name, varType, self.argOffset))
		self.numberOfArguments +=1

	# Add function 
	def addAttr(self, type, name, varType, x, y):
		self.table.append((type, name, varType, x, y))

		
	def getOffsetTable(self, name):
		for item in self.table:
			try:
				(type, varname, varType, offset) = item
				if varname == name:
					return offset
			except:
				None
				#do nothing
		
	
	def lookuptable(self, name):
		for item in self.table:
			try:
				(type, varname, varType, offset) = item
				if varname == name:
					return item
			except:
				(type, varname, arguments, returnType, offset) = item
				if(varname == name):
					return item
		return None
	
	def getTypetable(self, name):
		for item in self.table:
			try:
				(type, varname, varType, offset) = item
				if varname == name:
					return varType
			except:
				None
				#do nothing
				
	def lookupFunTable(self, name):
		for item in self.table:
			try:
				(type, varname, arguments, returnType, offset) = item
				if(type == "Fun_attr" and varname == name):
					return True
			except:
				None
				
	def getFunRtype(self, name):
		for item in self.table:
			try:
				(type, varname, arguments, returnType, offset) = item
				if(type == "Fun_attr" and varname == name):
					return returnType
			except:
				None
			
	def getFunTable(self, name):
		for item in self.table:
			try:
				(type, varname, arguments, returnType, offset) = item
				if(type == "Fun_attr" and varname == name):
					return item
			except:
				None
				
				