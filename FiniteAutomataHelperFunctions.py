# Natalie Carlson
#CSCE 351 Homework 1
#Due: 02/19/2019

from itertools import chain, combinations as cmb
import copy



#helper functions
#####################################################################	
#determine all subsets of Q
def R(Q):
	return(chain.from_iterable(cmb(list(Q), i) for i in range (len(list(Q))+1)))

#typecast a given set to string type to allow manipulation
#Modified from code written by Kris Carroll
def set_to_string(set):
	set_string = ""
	set_list = list(set)#put elements into a list
	set_list.sort()#sort the elements
	if len(set_list) >= 1: #more than one element in the list
		for i in range(len(set_list)):
			set_string += str(set_list[i]) #typecast element and add to string
			if i < len(set_list) - 1:
				set_string += ", " #add comma between elements
	return set_string
		
######################################################################
#this is a reqursive function that will find all possible e-transition pathways from a given state
def close_eTran(delta, startq, temp):
	for q in startq:
		if q in delta.keys():
			if delta[q][None] != {}: #there is an e-transition
				temp.add(set_to_string(delta[q][None]))
				return close_eTran(delta, (delta[q][None]), temp)#make call to next e-transition
	return {set_to_string(temp)}
######################################################################
#add a new delta transition set
def add_newTran(delta, nS, Sigma):
	newS = set_to_string(nS)
	delta[newS]={}
	for letter in Sigma:
			delta[newS][letter] = {}
	delta[newS][None] = {}	
#########################################################################	
#add a new e-transition
def add_eTran(delta, fromS, toS):
	temp = {set_to_string(toS)}
	accept = set_to_string(fromS)
	for k1, v1 in dict(delta).items(): #k1=Q, v1=letter		
		for k2, v2 in dict(v1).items():#k2=letter, v2=qSet
			if k1 == accept and k2 == None:
				if v2 != {}: #not empty
					for q in v2:
						temp.add(q)
	delta[accept][None] = {set_to_string(temp)}	
######################################################		
# add new letters to delta transition sets
def add_letters(delta, SigmaS, SigmaU):
	for letter in SigmaU:
		if letter not in SigmaS:
			#temp = {set_to_string(letter)}
			for k1, v1 in dict(delta).items():
				delta[k1][letter]={}
#################################################################
#rename matching states names 
def removeDups(Q1, Q2, delta2, q02, F2):
	duplicates = [] #declare list of duplicates
	for q in Q1: #check all states in Q1
		if q in Q2:#find duplicates in Q2
			duplicates.append(q)#add to duplicate list
			Q2.remove(q) #remove from Q2
			Q2.add(q+'a') #add newly named to Q2
	#rename in delta2			
	for k1, v1 in dict(delta2).items(): #k1=Q, v1=letter
			for k2, v2 in dict(v1).items():#k2=letter, v2=qSet
				if v2 != {}:
					for q in v2:
						if q in duplicates:
							v2.add(q+'a')#update transition state name
							v2.remove(q)
			if k1 in duplicates:
				delta2[k1+'a']=v1 #update current state name
				del delta2[k1]
	#rename q02 and F2
	for q in q02:
		if q in duplicates:
			q02.add(q+'a')
			q02.remove(q)
	for q in F2:
		if q in duplicates:
			F2.add(q+'a')
			F2.remove(q)
			
#########################################################################
#Parsing code with minor modifications from:
#https://xysun.github.io/posts/regex-parsing-thompsons-algorithm.html

class Lexer:
	#create expression object (items: expression, list of possible symbols, index tracker, expression length)
	def __init__(self, expression):
		self.source = expression
		self.symbols = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'UNION', '\x08':'CONCAT'}
		self.current = 0
		self.length = len(self.source)
	
	#request new token object 
	def get_token(self): 
		if self.current < self.length: # if i < len(expression)
			c = self.source[self.current] # c = expression[i]
			self.current += 1 #i++
			if c not in self.symbols.keys(): # if c != operation
				token = Token('LETTER', c) # token = new Token object (name = 'CHAR', value = c)
			else:
				token = Token(self.symbols[c], c) # token = new Token object (name = 'symbolName', value = c)
			return token
		else:
			return Token('NONE', '') #error, past end of expression

class Parser:
	#create object of lexer parts
	def __init__(self, lexer): #(items: lexer, list of tokens, current token)
		self.lexer = lexer 
		self.tokens = []
		self.lookahead = self.lexer.get_token() #next token object
	
	def consume(self, name):
		if self.lookahead.name == name:
			self.lookahead = self.lexer.get_token()
		else:
			print("Error Ocurred")

	def parse(self):
		self.exp()#check exp
		return self.tokens
	
	def exp(self):
		self.term()#check term
		if self.lookahead.name == 'UNION':#handle union
			t = self.lookahead
			self.consume('UNION')
			self.exp()#recheck exp
			self.tokens.append(t)

	def term(self):
		self.factor()#check factor
		if self.lookahead.value not in ')|':
			self.term()#recheck term
			self.tokens.append(Token('CONCAT', '\x08'))#add concat
	
	def factor(self):
		self.primary()#check primary
		if self.lookahead.name == 'STAR':#handle star
			self.tokens.append(self.lookahead)
			self.consume(self.lookahead.name)

	def primary(self):#Subexpression
		if self.lookahead.name == 'LEFT_PAREN': #handle parenthesis
			self.consume('LEFT_PAREN') #self.lookahead = self.lexer.get_token() #request new token object 
			self.exp() #check exp
			self.consume('RIGHT_PAREN')
		elif self.lookahead.name == 'LETTER':
			self.tokens.append(self.lookahead)
			self.consume('LETTER')

class Token:
	#create token object (items: name ('LETTER' or Symbol name), value(actual char)
	def __init__(self, name, value): #create Token object
		self.name = name
		self.value = value

	def __str__(self):
		return self.name + ":" + self.value

