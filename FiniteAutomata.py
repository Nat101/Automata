# Natalie Carlson
#CSCE 351 Homework 1
#Due: 02/19/2019


from itertools import chain, combinations as cmb
from FiniteAutomataHelperFunctions import*


#1.  Output if DFA is valid	or not		
# Moddified from dfa_accept() provided by Dr. Lauter for assignment
def dfa_accept(M,w):
	(Q, Sigma, delta, q0, F) = M
	q = next(iter(q0))
	if q not in Q:
		return False
	
	# expanded delta function
	for letter in w: #s = w  while s!="": a = s[0] s = s[1:]
		if letter not in Sigma: # if a not in Sigma: return False
			return False
		try:
			#retrieve set of possible next state(s)
			q = next(iter(delta[q][letter])) #q = delta (q, a)
			if q not in Q:
				return False
		except:
			return False
		
	if q in F:
		return True
	return False


#2 NFA to DFA	
def nfa_toDFA(N):
	(Q, Sigma, delta, q0, F) = copy.deepcopy(N)
	
	#QP is the Power set of Q
	QP = set()
	Qlist = list(R(Q))#make list of all possible subset
	Qlist.sort()
	for i in range(len(Qlist)):
		QP.add(set_to_string(Qlist[i]))#add subsets to QP
	
	#SigmaP is the same
	SigmaP = Sigma
	
	#start state is q0P and all states q0P can get to from e-transitions
	q0P = close_eTran(delta, q0, {set_to_string(q0)})
	
	#new delta
	deltaP = {}
	deltaP.update(delta)#add NFAdelta
	#close e-transitions on all states
	for k1, v1 in dict(deltaP).items(): #k1=Q, v1=letter		
		for k2, v2 in dict(v1).items():#k2=letter, v2=qSet
			if v2 != {}: #not empty
				temp = close_eTran(deltaP, v2, {set_to_string(v2)})
				deltaP[k1][k2] = temp
				
	#add additional transitions
	for sets in QP:
		if sets not in Q and sets !='':
			subSet = set([x.strip()for x in sets.split(',')])
			subSet_String = set_to_string(subSet)
			add_newTran(deltaP, subSet, SigmaP)
			for l in SigmaP:
				temp = set()
				for q in subSet:
					if q in deltaP.keys() and l in deltaP[q].keys():
						if deltaP[q][l] != {}:
							s = (set_to_string(set(deltaP[q][l])))
							temps = set([x.strip()for x in s.split(',')])
							for t in temps:
								if t not in temp:
									temp.add(t)
				deltaP[subSet_String][l] = {set_to_string(temp)}
							
	FP = set()
	#FP is all sets of QP that contain F
	for sets in QP: #check all sets
		for q in sets:
			if q == set_to_string(F):
				FP.add(sets)
			
	#remove e-transitions
	for k1, v1 in dict(deltaP).items():
		for k2, v2 in dict(v1).items():
			if k2 is None:
				del v1[k2]
	
	dfa = (QP, SigmaP, deltaP, q0P, FP)
	return dfa



#3 Take two NFAs and return an NFA of their union	
def nfa_union(N1,N2):
	
	#deep copy to prevent changing original in main
	(Q1, Sigma1, delta1, q01, F1) = copy.deepcopy(N1) 	
	(Q2, Sigma2, delta2, q02, F2) = copy.deepcopy(N2)
	
	
	#if machine N1 and N2 have matching state names then rename duplicates in N2
	removeDups(Q1, Q2, delta2, q02, F2)
					
	#start union
	nfaUnion = ()#new machine	
	q0 = {'S'} #new start state
	F = {'F'} #new acceptState
	
	Q = Q1.union(Q2) #add Q1 and Q2 states
	Q = Q.union(q0)#add new start state
	Q = Q.union(F)#add new accept state
	
	Sigma = Sigma1.union(Sigma2) #union alphabet
	
	delta = {} #new delta
	add_newTran(delta, q0, Sigma)#add new start
	add_newTran(delta, F, Sigma)#add new accept
	#add new e-transitions
	add_eTran(delta, q0, q01)#from new start state to N1 start
	add_eTran(delta, q0, q02)#from new start state to N2 start
	add_eTran(delta1, F1, F) #from delta1 accept to new accept	
	add_eTran(delta2, F2, F) #from delta2 accept to new accept
	#add new letters
	add_letters(delta1, Sigma1, Sigma)
	add_letters(delta2, Sigma2, Sigma)
	#add update delta1 and delta2
	delta.update(delta1) 
	delta.update(delta2)
					
	nfaUnion = (Q, Sigma, delta, q0, F)	
	return nfaUnion
	
#4 Take two NFAs and return an NFA of their concatenation
def nfa_concat(N1,N2):
	(Q1, Sigma1, delta1, q01, F1) = copy.deepcopy(N1)
	(Q2, Sigma2, delta2, q02, F2) = copy.deepcopy(N2)


	#if machine N1 and N2 have matching state names then rename duplicates in N2
	removeDups(Q1, Q2, delta2, q02, F2)

	q0 = q01
	F = F2
	delta1[set_to_string(F1)][None]={set_to_string(q02)} #accept state N1 to start state N2

	Q = Q1.union(Q2)
	Sigma = Sigma1.union(Sigma2)
	
	delta = {}
	delta.update(delta1)
	delta.update(delta2)

	nfaConcat = (Q, Sigma, delta, q0, F)	
	return nfaConcat

#5 Take an NFA and returns an NFA of its Star
def nfa_star(N):
	(Q, Sigma, delta, q0, F) = copy.deepcopy(N)
	
	q0S = {'S'} #new start state
	FS = {'F'} #new acceptState
	
	#new Q
	#QS = set()	
	#QS= QS.union(Q) #add previous Q
	QS = Q
	QS = QS.union(q0S) #add new start
	QS = QS.union(FS) #add new accept
		
	SigmaS = Sigma
	
	deltaS = {} #new delta
	deltaS.update(delta) 
	add_newTran(deltaS, q0S, SigmaS)#add new start
	add_newTran(deltaS, FS, SigmaS)#add new accept
	#add new e-transitions
	add_eTran(deltaS, q0S, q0)#from new start state to q0 start
	add_eTran(deltaS, q0S, FS)#from new start state to new accept
	add_eTran(deltaS, F, q0) #from delta accept to q0 start	
	add_eTran(deltaS, F, FS) #from delta accept to new accept
	
	nfaStar = (QS, SigmaS, deltaS, q0S, FS)	
	
	return nfaStar

#6 regular expression to NFA
def reg_toNFA(expression):
	
	Q = set()
	q0 = ('S')
	F = ('F')
	Q.add(q0)
	Q.add(F)
	Sigma = set()
	delta = {}
	NFA = (Q, Sigma, delta, q0, F)
	
	#parse expression
	lexer = Lexer(expression)#send expression to lexer
	parser = Parser(lexer)#send expression object to parser
	tokens = parser.parse()
	
	letterStack= []
	opStack = []
	#retrieve tokens
	for t in tokens:
		if(t.name[0] == 'L'):
			Sigma.add(t.value)#add to Sigma
			letterStack.append(t.value)#add to letter stack
		else:
			opStack.append(t.value)#add to op stack
			
	#develop delta
	delta[q0]= {}
	delta[F]= {}
	for l in Sigma:
		delta[q0][l]={}
		delta[F][l]={}
	delta[q0][None]={'0'}
	delta[F][None]={}

	stateCount = 0
	prevOP = ''
	prevLet = ''
	while len(opStack) > 0 and len(letterStack) > 0:
		
		op = opStack.pop(0) #get next operation
				
		if op == '|': #union
			letter1 = letterStack.pop(0)
			letter2 = letterStack.pop(0)
			letterStack.insert(0,letter2)#put back on top of stack for next operation
			
			if prevOP != '|' and prevOP != '*': #union with concat expression
				delta[str(stateCount-2)][letter2] = str(stateCount + 1)
				stateCount = stateCount + 1	
			
			prevOP = op
				
		elif op == '*':#star
			
			letter1 = letterStack.pop(0)
			letterStack.insert(0,letter1) #put back on top of stack for next operation
									
			delta[str(stateCount)]={}
			for l in Sigma:
				delta[str(stateCount)][l]={}
			delta[str(stateCount)][None]={}
			delta[str(stateCount)][letter1]= str(stateCount) #stay in state
			stateCount = stateCount + 1
			
			prevOP = op
			
		else: #concat
			if len(letterStack) == 1: #ignore extra concat
				letterStack.pop(0)
				break
			
			letter1 = letterStack.pop(0)
			letter2 = letterStack.pop(0)
			letterStack.insert(0,letter2)#put back on top of stack for next operation
			
			if stateCount == 0: #first operation
				delta[str(stateCount)]={}
				for l in Sigma:
					delta[str(stateCount)][l]={}
				delta[str(stateCount)][None]={}
				delta[str(stateCount)][letter1]= str(stateCount + 1)
				stateCount = stateCount + 1

				delta[str(stateCount)]={}
				for l in Sigma:
					delta[str(stateCount)][l]={}
				delta[str(stateCount)][None]={}
				delta[str(stateCount)][letter2]= str(stateCount + 1)
				stateCount = stateCount + 1
			
			elif prevOP == '|': #concat with union 
				delta[str(stateCount-1)]={}
				for l in Sigma:
					delta[str(stateCount-1)][l]={}
				delta[str(stateCount-1)][None]={}
				delta[str(stateCount-1)][letter2]= str(stateCount + 1)
				delta[str(stateCount)]={}
				for l in Sigma:
					delta[str(stateCount)][l]={}
				delta[str(stateCount)][None]={}
				delta[str(stateCount)][letter2]= str(stateCount + 1)
				stateCount = stateCount + 1

			else:
				delta[str(stateCount-1)][letter2]= str(stateCount)
				stateCount = stateCount + 1
			
			prevOP = op
			
	#e-transitions from start and to accept
	delta[str(stateCount-1)]={}
	for l in Sigma:
		delta[str(stateCount-1)][l]={}
	delta[str(stateCount-1)][None] = F
	for i in range(stateCount-1):
		Q.add(str(i))
	
	return (NFA)

#7
def isReg(expression, s):
	
	rNFA = reg_toNFA(expression)
	convertR1 = nfa_toDFA(rNFA)
	return dfa_accept(convertR, s)
	