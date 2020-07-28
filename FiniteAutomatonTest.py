# Natalie Carlson
#CSCE 351 Homework 1
#Due: 02/19/2019
#Tester for CSCE 351 Homework 1
from FiniteAutomata import* 
from itertools import chain, combinations as cmb


#############################################################
#DFAs
#Delta functions
delta_odd = {
'0':{ '0':{'0'}, '1':{'1'} },
'1':{ '0':{'1'}, '1':{'0'} }
}
delta_323 = {
'5':{ '2':{'5'}, '3':{'6'} },
'6':{ '2':{'7'}, '3':{'6'} },
'7':{ '2':{'5'}, '3':{'8'} },
'8':{ '2':{'8'}, '3':{'8'} }
}
delta_so = {
'0':{ '0':{'0'}, '1':{'1'}},
'1':{ '0':{'2'}, '1':{'0'}},
'2':{ '0':{'1'}, '1':{'2'}}
}
#M = {Q, Sigma, Delta, q0, F}
M1 = ({'0', '1'}, {'0', '1'}, delta_odd, {'0'}, {'0'})
M2 = ({'5', '6', '7', '8'}, {'2', '3'}, delta_323, {'5'}, {'8'})
M3 = ({'0', '1', '2'}, {'0', '1'}, delta_so, {'0'}, {'0'})
#test strings
oddT = "0001010101011"
oddF = "0001010101010"
three23T = "223332322333322"
three23F = "223332232233322"
soT = "1001"
soF = "101"
#tests
print("\nTest 1 DFA:")
print("Testing oddT on M1: ", dfa_accept(M1, oddT))
print("Testing oddF on M1: ", dfa_accept(M1, oddF))
print("Testing three23T on M2:", dfa_accept(M2, three23T))
print("Testing three23F on M2:", dfa_accept(M2, three23F))
print("Testing soT on M3:", dfa_accept(M3, soT))
print("Testing soF on M3:", dfa_accept(M3, soF))
############################################################

#NFAs
#Delta functions
delta_241 = {
'1':{ '0':{'1'}, '1':{'1','2'}, None:{}    }, 
'2':{ '0':{'3'}, '1':{},        None:{'3' } },
'3':{ '0':{},    '1':{'4'},     None:{}    },
'4':{ '0':{'4'}, '1':{'4'},     None:{}    },
}		
delta_251 = {  
'1':{ 'a':{'3'}, 'b':{},        None:{'2'} }, 
'2':{ 'a':{'1'}, 'b':{},        None:{}    },
'3':{ 'a':{'2'}, 'b':{'2','3'}, None:{}    }
}
delta_condor = {
'1':{ 'a':{'3'},     'b':{},     None:{'5'} },
'2':{ 'a':{'4', '5'}, 'b':{},    None:{}    },
'3':{ 'a':{},         'b':{'4'}, None: {}   },
'4':{ 'a':{'5'},      'b':{'5'}, None:{}    },
'5':{ 'a':{},         'b':{},    None:{}    }
}
# N = {Q, Sigma, Delta, q0, F}
N1 = ({'1','2','3','4'}, {'0', '1'}, delta_241, {'1'}, {'4'})
N2 = ({'1','2','3'}, {'a','b'}, delta_251, {'1'}, {'2'})
N3 = ({'1', '2', '3', '4', '5'}, {'a', 'b'}, delta_condor, {'1'}, {'5'})
#test strings
t241 = "010110"
f241 = "010"
t251 = "aa"
f251 = "b"
tcondor = "aba"
tcondor2 = "abb"
fcondor = "bbba"
#tests
print("\nTest 2 NFA to DFA:")
convert1 = nfa_toDFA(N1)
#print("Testing on N1: new DFA: ", convert1)
print("Testing t241 on converted N1", dfa_accept(convert1, t241))
print("Testing f241 on converted N1", dfa_accept(convert1, f241))
convert2 = nfa_toDFA(N2)
#print("Testing on N2: new DFA: ", convert2)
print("Testing t251 on converted N2", dfa_accept(convert2, t251))
print("Testing f251 on converted N2", dfa_accept(convert2, f251))
convert3 = nfa_toDFA(N3)
#print("Testing on N3: new DFA: ", convert3)
print("Testing tcondor on converted N3", dfa_accept(convert3, tcondor))
print("Testing tcondor2 on converted N3", dfa_accept(convert3, tcondor2))
print("Testing fcondor on converted N3", dfa_accept(convert3, fcondor))

print("\nTest 3 NFA union:")
uN1N3 = nfa_union(N1,N3)
convertU = nfa_toDFA(uN1N3)
print("Testing tcondor on uN1N3: ", dfa_accept(convertU, tcondor))
print("Testing t241 on uN1N3: ", dfa_accept(convertU, t241))
print("Testing fcondor on uN1N3: ", dfa_accept(convertU, fcondor))
print("Testing f241 on uN1N3: ", dfa_accept(convertU, f241))

print("\nTest 4 NFA concat:")
cN1N3 = nfa_concat(N1,N3)
convertC = nfa_toDFA(cN1N3)
print("Testing t241+tcondor on cN1N3: ", dfa_accept(convertC, t241+tcondor))
print("Testing f241+fcondoron cN1N3: ", dfa_accept(convertC, f241+fcondor))

print("\nTest 5 NFA star:")
sN3 = nfa_star(N3)
convertS = nfa_toDFA(sN3)
print("Testing  condorStarT sN3: ", dfa_accept(convertS, ''))


#################################################

#Regex
expression1 = "(a|b)*c|(a|ab)*c"
expression2 = "(ab|a)(bc|c)"
expression3 = "((a|a)|a)"
#test strings
string1T = "abc" 
string1F = "bbbcabbbc"
string2T = "abc"
string2F = "acb"
string3T = "a"
string3F =  "aa"

#tests
print("\nTest 6 Regex to NFA")
rNFA1 = reg_toNFA(expression1)
rNFA2 = reg_toNFA(expression2)
rNFA3 = reg_toNFA(expression3)

print("\Test 7 Bool Regex String")
isReg(expression1, string1T)
isReg(expression1, string1F)

