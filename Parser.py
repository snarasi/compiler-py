#!/usr/bin/python
#The semantics program will incorporate the three generic types: semantic stack manipulation, symbol
#table manipulation and the generation of intermediate code called 4-tuples
import Config
from SemanticsAnalyzer import SemanticsAnalyzer

class Parser:
    
    def __init__(self):
        self.parseStack = []
        self.reductions = {}
        self.symbols = []
        self.prepareWpMatrix()
        self.prepareReduction()
        self.prepareSymbols()
        self.inPanicMode = False
        self.lastPushedSymbol = ''
        self.lastPushedIndex = 0
        self.lastPushedIndexCalculated = False
        self.ignoredSymbolsInCaseOfPanicMode = []
        self.sem_obj = SemanticsAnalyzer()
        pass
        
    def processToken(self, tokenTuple):
        if (self.inPanicMode):
            self.getIntoPanicMode(tokenTuple[0],'0')
        else:
            self.parse(tokenTuple)        
    
    def prepareSymbols(self):
        file = open('symbols', 'r') 
        for line in file:
            line = line.strip()
            self.symbols.append(line)  
    
    def prepareReduction(self):
        file = open('sorted_reductions', 'r')        
        for line in file:
            list = line.split()
            list = map(int, list)
            count = list[0]+1
            if not self.reductions.has_key(list[count]):        
                self.reductions[list[count]] = []
            self.reductions[list[count]].append(list[1:])
        pass
        
    def prepareWpMatrix(self):
        f = open('wpmat', 'r')
        self.wpmat = [None] * 84
        for i in range(84):
            self.wpmat[i] = [None] * 84        
        for i in range(84):
            line = f.readline()
            for j in range(84):
                self.wpmat[i][j] = line[j]        
        for i in range(84):
            for j in range(84):
                pass                
            
    def parse(self, token):     
        if len(self.parseStack) == 0:           
            self.parseStack.append(token)
            self.sem_obj.push(token[0])
        else:                        
            valueFromStack = self.parseStack[-1]
            if (self.wpmat[valueFromStack[1]][token[1]] == '0'):
                self.inPanicMode = True
                self.getIntoPanicMode(token[0],'0')
            else:
                self.printTopOfStackInputAndRelation(valueFromStack[1],token[1],self.wpmat[valueFromStack[1]][token[1]])
                if (self.wpmat[valueFromStack[1]][token[1]] == '1' or self.wpmat[valueFromStack[1]][token[1]] == '3'):
                    self.parseStack.append(token)
                    self.sem_obj.push(token[0])
                else:
                    if(self.wpmat[valueFromStack[1]][token[1]] == '2'):
                        for item in self.reductions[valueFromStack[1]]:
                            stack = []
                            for i in range(len(self.parseStack)):
                                stack.append(self.parseStack[i][1])
                            if (len(stack[-(len(item[1:-1])):])==len(item[1:-1]) and item[1:-1] == stack[-(len(item[1:-1])):]):
                                self.printStack()
                                self.printSemanticStack("(before)")                        
                                self.printMatchedHandle(item[1:-1])
                                self.printReduction(item)                                                                                                            
                                
                                # call semantics function
                                self.sem_obj.analyze(item[0])                                
                                # parser reduce               
                                del(self.parseStack[-(len(item[1:-1])):])                                                             
                                self.parseStack.append([token[0],item[-1]])                                
                                # make semantic stack length equal to syntax stack                             
                                del(self.sem_obj.the_semantic_stack[len(self.parseStack):])
                                
                                if not self.lastPushedIndexCalculated:
                                    self.lastPushedIndex = len(self.parseStack)-1
                                    self.lastPushedIndexCalculated = True
                                self.printStack()
                                self.printSemanticStack("(after) ")                                                   
                                self.parse(token)
                                break
                        else:
                            self.inPanicMode = True
                            self.getIntoPanicMode(token[0],'0')

    def parseLast(self):
        if len(self.parseStack) > 0:
            valueFromStack = self.parseStack[-1]
            for item in self.reductions[valueFromStack[1]]:
                stack = []
                for i in range(len(self.parseStack)):
                    stack.append(self.parseStack[i][1])
                if (len(stack[-(len(item[1:-1])):])==len(item[1:-1]) and item[1:-1] == stack[-(len(item[1:-1])):]):
                    self.printStack()
                    self.printSemanticStack("(before)")                 
                    self.printMatchedHandle(item[1:-1])
                    self.printReduction(item)                                                        
                    self.sem_obj.analyze(item[0])                    
                    del(self.parseStack[-(len(item[1:-1])):])                             
                    del(self.sem_obj.the_semantic_stack[len(self.parseStack):])                    
                    if not self.lastPushedIndexCalculated:
                        self.lastPushedIndex = len(self.parseStack)-1
                        self.lastPushedIndexCalculated = True
                    self.printStack()
                    self.printSemanticStack("(after) ")
                    self.sem_obj.print_global_symbol_table()
                    print "Parse Complete"
                    break
            else:
                self.inPanicMode = True
                self.getIntoPanicMode(0,'0')

    def printMatchedHandle(self, reductionItem ):
        if Config.flags[10]:
            str = "\t\tMatched Handle:"
            for i in reductionItem:
                str = str + " "  + (self.symbols[i-1]);                
            print str                    

    def printReduction(self, reductionItem ):
        if Config.flags[7]:            
            strng = "\t\t"+str(reductionItem[0])+") "+self.symbols[reductionItem[-1]-1] + " --> "            
            for i in reductionItem[1:-1]:
                strng = strng + " "  + (self.symbols[i-1]);                  
            print strng

    def printStack(self):
        if Config.flags[8]:
            list = []
            for i in range(len(self.parseStack)):
                list.append(self.symbols[self.parseStack[i][1]-1])
            for i in range(1, len(list)):
                list.insert(i*2-1, '|')            
            print "\t\tStack:",''.join(list)
            
    def printSemanticStack(self, position):
        if Config.flags[12]:
            list = []
            for i in range(len(self.sem_obj.the_semantic_stack)):
                list.append(self.sem_obj.the_semantic_stack[i])
            for i in range(1, len(list)):
                list.insert(i*2-1, '|')
            printstring = "\t\tSemantic Stack"+position+":"
            print printstring,''.join(list)
            
    def printTopOfStackInputAndRelation(self,topOfTheStack,inputSymbol,relation):
        if Config.flags[9]:
            if (relation == '1'):
                rel = '='
            elif (relation == '2'):
                rel = '>'
            else:
                rel = '<'
            print "\t\tRelation:",self.symbols[topOfTheStack-1],rel,self.symbols[inputSymbol-1]
        
    def getIntoPanicMode(self,inputSymbol,relation):
        if (inputSymbol == ';'):
            self.ignoredSymbolsInCaseOfPanicMode.append(inputSymbol)                      
            stack = []
            for i in range(len(self.parseStack)):
                stack.append(self.parseStack[i][0])
            if (relation == '0'):
                print "Character Pair error in line",Config.line_number,"between",stack[-1],"and",self.ignoredSymbolsInCaseOfPanicMode[0]
            del(self.ignoredSymbolsInCaseOfPanicMode[0])
            print "Symbols ignored in the rest of the line:",' '.join(self.ignoredSymbolsInCaseOfPanicMode)         
            print "Symbols popped from the stack:",' '.join(stack[self.lastPushedIndex+1:])                            
            del(self.parseStack[self.lastPushedIndex+1:])            
            del(stack[:])
            for i in range(len(self.parseStack)):
                stack.append(self.symbols[self.parseStack[i][1]-1]) 
            for i in range(1, len(stack)):
                stack.insert(i*2-1, '|')
            print "Stack:",''.join(stack)
            
            del(self.ignoredSymbolsInCaseOfPanicMode[:])
            self.inPanicMode = False
        else:
            self.ignoredSymbolsInCaseOfPanicMode.append(inputSymbol)
            
    def startOfSomethingNew(self):
        self.lastPushedIndex = len(self.parseStack)
        self.lastPushedIndexCalculated = False
