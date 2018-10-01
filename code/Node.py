class Node(object):
	
	def __init__(self, name):
		self.name = name
		self.children = []
		self.attributes = []
		
	def addChild(self, child):
		self.children.append(child)
	
	def addAttribute(self, attribute):
		self.attributes.append(attribute)
	
	def addChildren(self, input):
		new = self.flatten(input)
		for node in new:
			if node is not None:
				self.addChild(node)
		
	def flatten(self, T):
		if not isinstance(T, tuple):
			return (T,)
		elif len(T) == 0: 
			return ()
		else:
			return self.flatten(T[0]) + self.flatten(T[1:])
			
	def rename(self, name):
		self.name = name
		
	def delete(self, name):
		for child in self.children:
			if child.name == name:
				children.remove(child)
		