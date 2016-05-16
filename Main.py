#!/usr/bin/python
# Main Program to be executed which calls the various modules - Lexical analysis, Semantics parser and pragmatics to convert 
# tuples into machine level code using NASM.
from LexicalAnalyzer import LexicalAnalyzer
from Parser import Parser
import re, sys, string
import Config
from pragma import Pragmatic


if __name__ == "__main__":
    if len(sys.argv) != 2: # the program name and the file name argument        
        sys.exit("Must provide file name!") # stop the program and print an error message
    Config.file_name = sys.argv[1]
    Config.PragmaticAnalyzer = Pragmatic()

    parser = Parser()
    lexicalAnalyzer = LexicalAnalyzer()
    lexicalAnalyzer.setParser(parser)   
    import datetime
    from time import gmtime, strftime
    print "executed at : ",strftime("%Y-%m-%d %H:%M:%S")
    print ""    
    f = open(sys.argv[1], 'r')    
    for line in f:
        Config.line_number+= 1        
        if Config.flags[1]:
            print "Source Line : ", line[:-1].strip()
        parser.startOfSomethingNew()
        result = lexicalAnalyzer.lex(line)          
    parser.parseLast()
    Config.PragmaticAnalyzer.add_declaration_section()
