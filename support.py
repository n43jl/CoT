#!/usr/bin/python

__doc__='''Support functions for visiting the AST
These functions expose high level interfaces (passes) for actions that can be applied to multiple IR nodes.'''

import ir

def get_node_list(root):
	'''Get a list of all nodes in the AST'''
	def register_nodes(l):
		def r(node):
			if node not in l :
				l.append(node)
		return r
	node_list = []
	root.navigate(register_nodes(node_list))
	return node_list	

def get_symbol_tables(root):
	'''Get a list of all symtabs in the AST'''
	def register_nodes(l):
		def r(node):
			try : 
				if node.symtab not in l : l.append(node.symtab)
			except Exception : pass
			try : 
				if node.lc_sym not in l : l.append(node.symtab)
			except Exception : pass
		return r
	node_list = []
	root.navigate(register_nodes(node_list))
	return node_list	
	

def lowering(node):
	'''Lowering action for a node
	(all high level nodes can be lowered to lower-level representation'''

	# no need
	if (isinstance(node, ir.Block) or isinstance(node, ir.StatList) or
			isinstance(node, ir.LoadArrStat) or isinstance(node, ir.DefinitionList) or
			isinstance(node, ir.BinStat) or isinstance(node, ir.LoadStat) or
			isinstance(node, ir.StoreArrStat) or isinstance(node, ir.StoreStat) or
			isinstance(node, ir.PrintStat) or isinstance(node, ir.CallStat) or 
			isinstance(node, ir.BranchStat) or
			isinstance(node, ir.EmptyStat)):
		return

	check=node.lower()
	print 'Lowering', type(node), id(node)
	if not check : 
		print 'Failed!'

def flattening(node):
	'''Flattening action for a node 
	(only StatList nodes are actually flattened)'''
	try :
		check=node.flatten()
		print 'Flattening', type(node), id(node)
		if not check : 
			print 'Failed!'
	except Exception, e :
		#print type(node), e
		pass # this type of node cannot be flattened


def dotty_wrapper(fout):
	'''Main function for graphviz dot output generation'''
	def dotty_function(irnode):
		from string import split, join
		from ir import Stat
		attrs = set(['body','cond', 'thenpart','elsepart', 'call', 'step', 'expr', 'target', 'defs' ]) & set(dir(irnode))
	
		res=`id(irnode)`+' ['
		if isinstance(irnode,Stat):
			res+='shape=box,'
		res+='label="'+`type(irnode)`+' '+`id(irnode)`
		try :	res+=': '+irnode.value
		except Exception : pass
		try :	res+=': '+irnode.name
		except Exception : pass
		try : res+=': '+getattr(irnode,'symbol').name
		except Exception : pass
		res+='" ];\n'
	
		if 'children' in dir(irnode) and len(irnode.children) :
			for node in irnode.children :
				res+=`id(irnode)`+' -> '+`id(node)`+' [pos='+`irnode.children.index(node)`+'];\n'
				if type(node) == str :
					res+=`id(node)`+' [label='+node+'];\n'
		for d in attrs :
			node=getattr(irnode,d)
			if d == 'target' :
				res+=`id(irnode)`+' -> '+`id(node.value)`+' [label='+node.name+'];\n'
			else :
				res+=`id(irnode)`+' -> '+`id(node)`+';\n'
		fout.write(res)
		return res
	return dotty_function

def print_dotty(root,filename):
	'''Print a graphviz dot representation to file'''
	fout = open(filename,"w")
	fout.write("digraph G {\n")
	node_list=get_node_list(root)
	dotty=dotty_wrapper(fout)
	for n in node_list: dotty(n)
	fout.write("}\n")
