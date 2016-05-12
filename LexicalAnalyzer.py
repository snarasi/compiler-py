#!/usr/bin/python
import re, sys, string
import Config

class LexicalAnalyzer:

    def __init__(self):
        self.in_multi_comment = False
        self.codeline = " "
        self.tokens = {}        
        self.createTokens()
        Config.flags[1] = True

    def setParser(self, parser):
        self.parserDelegate = parser
    
    def parseToken(self, tokenTuple):
        self.parserDelegate.processToken(tokenTuple)
        
    def lex(self,line):        
        result = []
               
        regx = re.compile(r'(?P<headers>##[ \t]*([+|\-][0-9]|[+|\-][1-2][0-9]|[+|\-][3][0-2])*.*)|'
                          r'(?P<string>"[^"]*")|'
                          r'(?P<reservedWords>[A-Z]+)|'
                          r'(?P<multilinecomment>/\*.*\*/)|'
                          r'(?P<multilinecommentstart>[/][*].*)|'
                          r'(?P<multilinecommentend>[^"|^/*]*[\*][\/])|'
                          r'(?P<identifiers>[a-z][\w]*)|'
                          r'(?P<reals>-?\d+\.\d+)|'
                          r'(?P<integers>-?\d+)|'
                          r'(?P<multipleAsciiCharacter>==|!=|<=|>=|<-|::)|'
                          r'(?P<singlelinecomment>//.*)|'
                          r'(?P<asciiCharacters>[^\w\s])')
        
        iterator =  re.finditer(regx, line )
        for matchedObj in iterator:                   
            
            if self.in_multi_comment:
                regx = re.compile(r'(?P<end>.*?[*][/])')
                if regx.search(line):
                    x = string.replace(line, regx.search(line).group(), "")
                    print x
                    self.lex(x)
                    self.in_multi_comment = False    
            else:
                if matchedObj.group('headers'):
                    self.processGroupHeaders(matchedObj.group('headers'))
               
                if matchedObj.group('string'):
                    res = self.processString(matchedObj.group('string'))
                    if res:
                        result.extend(res)
                        self.parseToken(res)
                        
                if matchedObj.group('multilinecommentstart'):
                    self.in_multi_comment = True
                    
                if matchedObj.group('reservedWords'):
                    res = self.processReservedWords(matchedObj.group('reservedWords'))
                    if res:
                        result.extend(res)
                        self.parseToken(res)
                
                if matchedObj.group('identifiers'):
                    res = self.processIdentifiers(matchedObj.group('identifiers'))
                    if res:
                        result.extend(res)
                        self.parseToken(res)
                    
                if matchedObj.group('integers'):
                    res = self.processIntegers(matchedObj.group('integers'))
                    if res:                        
                        result.extend(res)
                        self.parseToken(res)
                    
                if matchedObj.group('reals'):
                    res = self.processReals(matchedObj.group('reals'))
                    if res:
                        result.extend(res)
                        self.parseToken(res)
            
                if matchedObj.group('multipleAsciiCharacter'):
                    res = self.processMultipleASCII(matchedObj.group('multipleAsciiCharacter'))
                    if res:
                        result.extend(res)
                        self.parseToken(res)
            
                if matchedObj.group('asciiCharacters'):
                    res = self.processASCII(matchedObj.group('asciiCharacters'))
                    if res:
                        result.extend(res)
                        self.parseToken(res)
                    
        return result
    
    groupNames = []
    
    def processString(self, matchedString):
        tokenString = "Token : " + matchedString + " code : " + str(self.tokens['STRING'])
        self.printToken(tokenString)
        return [matchedString, self.tokens['STRING']]
       
    def processMultipleASCII(self, matchedString):
        if self.tokens.has_key(matchedString):
            tokenString = "Token : " + matchedString + " code : " + str(self.tokens[matchedString])
            self.printToken(tokenString)
            return [matchedString, self.tokens[matchedString]]
        else:
            tokenString = matchedString + " is not a valid multiple ascii character"
            self.printToken(tokenString)
            return None
    
    def processASCII(self, matchedString):
        if self.tokens.has_key(matchedString):
            tokenString = "Token : " + matchedString + " code : " + str(self.tokens[matchedString])
            self.printToken(tokenString)
            return [matchedString, self.tokens[matchedString]]
        else:        
            tokenString = matchedString + " is not a valid ascii character"
            self.printToken(tokenString)
            return None
             
    def processIdentifiers(self, matchedString):
        if len(matchedString) < 17:
            key = 'IDENTIFIER'
            tokenString = "Token : " + matchedString + " code : " + str(self.tokens[key])
            self.printToken(tokenString)
            return [matchedString, self.tokens['IDENTIFIER']]
        else:
            tokenString = matchedString + " is not a valid identifier"
            self.printToken(tokenString)
            return None
        
    def processIntegers(self, matchedString):
        if int(matchedString) > 0:
            if len(matchedString) < 10:
                tokenString = "Token : " + matchedString + " code : " + str(self.tokens['INTEGERNUMBER'])
                self.printToken(tokenString)
                return [matchedString, self.tokens['INTEGERNUMBER']]
            else:
                tokenString = matchedString + " is not a valid integer"
                self.printToken(tokenString)
                return None
        else:
            if len(matchedString) < 11:
                tokenString = "Token : " + matchedString + " code : " + str(self.tokens['INTEGERNUMBER'])
                self.printToken(tokenString)
                return [matchedString, self.tokens['INTEGERNUMBER']]
            else:
                tokenString = matchedString + " is not a valid integer"
                self.printToken(tokenString)
                return None
                
    def processReals(self, matchedString):
        regx = re.compile(r'-?0\.0*[1-9][0-9]{0,6}(?!\d)')    
        m = regx.match(matchedString)
        if regx.match(matchedString):
            tokenString = "Token : " + m.group() + " code : " + str(self.tokens['REALNUMBER'])
            self.printToken(tokenString)
            return [matchedString, self.tokens['REALNUMBER']]
        else:
            if len(matchedString) < 9:  
                tokenString = "Token : " + matchedString + " code : " + str(self.tokens['REALNUMBER'])
                self.printToken(tokenString)
                return [matchedString, self.tokens['REALNUMBER']]
            else:            
                tokenString = matchedString + " is not a valid real number"
                self.printToken(tokenString)
                return None
        
    def processReservedWords(self, matchedString):
        if self.tokens.has_key(matchedString):
            tokenString = "Token : " + matchedString + " code : " + str(self.tokens[matchedString])
            self.printToken(tokenString)
            return [matchedString, self.tokens[matchedString]]
        else:        
            tokenString = matchedString + " is not a valid reserved word"
            self.printToken(tokenString)
            return None
    
    def processGroupHeaders(self, matchedString):
        regx = re.compile(r'(?P<headers>([+-])([1-2][0-9]|[3][1-2]|[0-9]))')
        iterator =  re.finditer(regx, matchedString)
        for matchedObj in iterator:
            if matchedObj.group('headers'):
                if matchedObj.group(2) == '+':
                    if matchedObj.group(3) == '0':
                        Config.flags = [True]*32
                    else:                    
                        Config.flags[int(matchedObj.group(3))] = True
                else:
                    if matchedObj.group(3) == '0':
                        Config.flags = [False]*32
                    else:                                      
                        Config.flags[int(matchedObj.group(3))] = False              
                  
    def printToken(self, tokenString):
        if Config.flags[2]:
            print "\t\t\t\t", tokenString
        
    def createGroups(self):
        self.groupNames.append('comments')
    
    def createTokens(self):
        self.tokens = {'END':39,'PROGRAM':40,'DECLARE':42,
        'PROCEDURE':49,'VALUE':52,'REFERENCE':53,'MAIN':54,'INPUT':58,'OUTPUT':60,'CALL':61,'ELSE':62,
        'IF':63,'THEN':66,'DO':67,'WHILE':68,'INTEGER':46,'REAL':47,'IDENTIFIER':41,'INTEGERNUMBER':44,
        'REALNUMBER':83,'STRING':59,';':43,':':57,',':50,'[':55,']':56,'(':64,')':65,
        '<':73,'>':75,'!':72,'+':79,'-':80,'*':81,'/':82,'{':51,'}':48,'|':70,'&':71,'==':77,
        '!=':78,'<=':74,'>=':76,'<-':69,'::':45}  
