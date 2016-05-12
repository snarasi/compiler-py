#!/usr/bin/python
import Config
from pragma import Pragmatic

class SemanticsAnalyzer:
    def __init__(self) :
        self.the_semantic_stack = []
        self.procedure_stack = []
        self.global_symbol_table = {}
        self.local_symbol_table = {} 
        self.in_procedure = 'GLOBAL'
        self.integer_IRN_counter = -1
        self.real_IRN_counter = -1
        self.boolean_IRN_counter = -1
        self.label_IRN_counter = 0
        self.loop_stack = []
        self.pragmaticAnalyzer = Config.PragmaticAnalyzer
        
    def push(self, item) :
        self.the_semantic_stack.append(item)
    
    def pop(self) :
        return self.the_semantic_stack.pop()
    
    def isEmpty(self) :
        return (self.the_semantic_stack == [])
    
    def analyze(self, production_number):
        #print "analyze production number ", production_number
        func = getattr(self, "analyze_production_" + str(production_number), None)
        if callable(func):
            #print "analyze_production_" , str(production_number), " is callable"
            func()
        else:
            pass
            #print "analyze_production_" , str(production_number), " is not callable"

        
    def insert_into_symbol_table(self, key, value):
        if(self.in_procedure == 'GLOBAL'):
            if self.global_symbol_table.has_key(key):
                print "\t\tSEMANTICS ERROR:", key, "declared more than once!"
            else:
                self.global_symbol_table[key] = value
        else:
            if self.local_symbol_table[self.in_procedure][-1].has_key(key):
                print "\t\tSEMANTICS ERROR:", key, "declared more than once!"
            else:          
                self.local_symbol_table[self.in_procedure][-1][key] = value
        if Config.flags[15]:
            self.print_st_entry(value)
        
    def print_four_tuple(self, four_tuple):
        if Config.flags[13]:
            print "\t\tTuple is:", four_tuple
        self.pragmaticAnalyzer.do_pragmatic(four_tuple)
        
    def print_local_symbol_table(self):
        if Config.flags[14]:
            print "\t\tLocal ST is: "
            for table in self.local_symbol_table.itervalues():        
                for value in table[-1].itervalues():
                    self.print_st_entry(value)
    
    def print_global_symbol_table(self):
        if Config.flags[16]:
            print "\t\tGlobal ST is: "
            for value in self.global_symbol_table.itervalues():
                self.print_st_entry(value)
    
    def print_st_entry(self, entry):
        printline = "\t\tST ENTRY: [NAME:" + entry['NAME']
        if entry.has_key('TYPE'):
            printline += ", TYPE:" + entry['TYPE']
        if entry.has_key('SHAPE'):
            printline += ", SHAPE:" + entry['SHAPE']
        if entry.has_key('SIZE'):
            printline += ", SIZE:" + entry['SIZE']
        if entry.has_key('ROWS'):
            printline += ", ROWS:" + entry['ROWS']
        if entry.has_key('COLS'):
            printline += ", COLS:" + entry['COLS']
        if entry.has_key('CALLTYPE'):
            printline += ", CALLTYPE:" + entry['CALLTYPE']
        printline += "]"
        print printline
        
    def get_next_IRN(self, prefix):
        if prefix == 'I':
            self.integer_IRN_counter = self.integer_IRN_counter + 1
            return ('I$'+str(self.integer_IRN_counter))
        if prefix == 'R':
            self.real_IRN_counter = self.real_IRN_counter + 1
            return ('R$'+str(self.real_IRN_counter))
        if prefix == 'B':
            self.boolean_IRN_counter = self.boolean_IRN_counter + 1
            return ('B$'+str(self.boolean_IRN_counter))
        
    def get_current_IRN(self, prefix):
        if prefix == 'I':            
            return ('I$'+str(self.integer_IRN_counter))
        if prefix == 'R':
            return ('R$'+str(self.real_IRN_counter))
        if prefix == 'B':
            return ('B$'+str(self.boolean_IRN_counter))
    
    #1. start --> prog body END
    def analyze_production_1(self):
        four_tuple = (self.the_semantic_stack[-3],"END PROGRAM",None,None)
        self.print_four_tuple(four_tuple)        
    
    #2. prog --> PROGRAM var
    def analyze_production_2(self):
        self.the_semantic_stack[-2] = self.the_semantic_stack[-1]
    
    #3. body --> declpart procpart execpart
    def analyze_production_3(self):
        pass
    
    #4. body --> declpart execpart
    def analyze_production_4(self):
        pass
    
    #5. declpart --> DECLARE decllist END
    def analyze_production_5(self):
        four_tuple = (None,"END DECLARATIONS",None,None)
        self.print_four_tuple(four_tuple)
    
    #6. decllist --> decllist declstat ;
    def analyze_production_6(self):
        pass
    
    #7. decllist --> declstat ;
    def analyze_production_7(self):
        pass
    
    #8. declstat --> type var
    def analyze_production_8(self):
        dict = {'NAME':self.the_semantic_stack[-1],\
                'TYPE':self.the_semantic_stack[-2],\
                'SHAPE':'scalar'}
        self.insert_into_symbol_table(self.the_semantic_stack[-1], dict)
        four_tuple = (self.the_semantic_stack[-1],"MEMORY",1,None)
        self.print_four_tuple(four_tuple)
    
    #9. declstat --> type var integer
    def analyze_production_9(self):
        dict = {'NAME':self.the_semantic_stack[-2],\
                'TYPE':self.the_semantic_stack[-3],\
                'SHAPE':'vector',\
                'SIZE':self.the_semantic_stack[-1]}
        self.insert_into_symbol_table(self.the_semantic_stack[-2], dict)
        four_tuple = (self.the_semantic_stack[-2],"MEMORY",self.the_semantic_stack[-1],None)
        self.print_four_tuple(four_tuple)
    
    #10. declstat --> type var integer :: integer
    def analyze_production_10(self):
        dict = {'NAME':self.the_semantic_stack[-4],\
                'TYPE':self.the_semantic_stack[-5],\
                'SHAPE':'matrix',\
                'ROWS':self.the_semantic_stack[-3],\
                'COLS':self.the_semantic_stack[-1]}
        self.insert_into_symbol_table(self.the_semantic_stack[-4], dict)
        four_tuple = (self.the_semantic_stack[-4],"MEMORY",self.the_semantic_stack[-3],self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)
    
    #11. type --> INTEGER
    def analyze_production_11(self):
        self.the_semantic_stack[-1] = "integer"
    
    #12. type --> REAL
    def analyze_production_12(self):
        self.the_semantic_stack[-1] = "real"
    
    #13. procpart --> proclist
    def analyze_production_13(self):
        pass
    
    #14. proclist --> proclist proc
    def analyze_production_14(self):
        pass
    
    #15. proclist --> proc
    def analyze_production_15(self):
        pass
    
    #16. proc --> prochead declpart statlist END
    def analyze_production_16(self):
#        self.in_procedure = 'GLOBAL'
        self.print_local_symbol_table()
        self.local_symbol_table[self.in_procedure].pop()
        self.in_procedure = self.procedure_stack.pop()
        four_tuple = (self.the_semantic_stack[-4],"END PROCEDURE",None,None)
        self.print_four_tuple(four_tuple)       
#        self.print_local_symbol_table()
    
    #17. proc --> prochead statlist END
    def analyze_production_17(self):
#        self.in_procedure = 'GLOBAL'
        self.print_local_symbol_table()
        self.local_symbol_table[self.in_procedure].pop()
        self.in_procedure = self.procedure_stack.pop()
        four_tuple = (self.the_semantic_stack[-3],"END PROCEDURE",None,None)
        self.print_four_tuple(four_tuple)    
#        self.print_local_symbol_table()
    
    #18. prochead --> procname fparmlist }
    def analyze_production_18(self):
        four_tuple = (None,"END PARAMETER LIST",None,None)
        self.print_four_tuple(four_tuple)
    
    #19. prochead --> procname
    def analyze_production_19(self):
        four_tuple = (None,"NO FORMAL PARAMETERS",None,None)
        self.print_four_tuple(four_tuple)
    
    #20. procname --> PROCEDURE var
    def analyze_production_20(self):
        dict = {'NAME':self.the_semantic_stack[-1],\
                'TYPE':'procedure'}
        self.insert_into_symbol_table(self.the_semantic_stack[-1], dict)
        self.procedure_stack.append(self.in_procedure)
        self.in_procedure = self.the_semantic_stack[-1]        
#        self.local_symbol_table.clear()
        dict = {'NAME':self.the_semantic_stack[-1],\
                'TYPE':'procedure'}
        if not self.local_symbol_table.has_key(self.the_semantic_stack[-1]):
            self.local_symbol_table[self.the_semantic_stack[-1]] = []
        new_local_table = {}
#        self.local_symbol_table[self.the_semantic_stack[-1]] = {}
        self.local_symbol_table[self.the_semantic_stack[-1]].append(new_local_table)
        dict = {'NAME':self.the_semantic_stack[-1],\
                'TYPE':'procedure'}
        self.insert_into_symbol_table(self.the_semantic_stack[-1], dict)
        four_tuple = (self.the_semantic_stack[-1],"BEGIN PROCEDURE",None,None)
        self.print_four_tuple(four_tuple)
        self.the_semantic_stack[-2] = self.the_semantic_stack[-1]
    
    #21. fparmlist --> fparmlist , calltype type var  
    def analyze_production_21(self):
        dict = {'NAME':self.the_semantic_stack[-1],\
                'TYPE':self.the_semantic_stack[-2],\
                'SHAPE':'scalar',\
                'CALLTYPE':self.the_semantic_stack[-3]}
        self.insert_into_symbol_table(self.the_semantic_stack[-1], dict)        
        four_tuple = (self.the_semantic_stack[-1],\
                      "FORMAL "+self.the_semantic_stack[-3].upper()+" PARAMETER",\
                      1,\
                      None)
        self.print_four_tuple(four_tuple)
    
    #22. fparmlist --> fparmlist , calltype type var integer
    def analyze_production_22(self):
        dict = {'NAME':self.the_semantic_stack[-2],\
                'TYPE':self.the_semantic_stack[-3],\
                'SHAPE':'vector',\
                'CALLTYPE':self.the_semantic_stack[-4],\
                'SIZE':self.the_semantic_stack[-1]}
        self.insert_into_symbol_table(self.the_semantic_stack[-2], dict)
        four_tuple = (self.the_semantic_stack[-2],\
                      "FORMAL "+self.the_semantic_stack[-4].upper()+" PARAMETER",\
                      self.the_semantic_stack[-1],\
                      None)
        self.print_four_tuple(four_tuple)
    
    #23. fparmlist --> fparmlist , calltype type var integer :: integer
    def analyze_production_23(self):
        dict = {'NAME':self.the_semantic_stack[-4],\
                'TYPE':self.the_semantic_stack[-5],\
                'SHAPE':'matrix',\
                'CALLTYPE':self.the_semantic_stack[-6],\
                'ROWS':self.the_semantic_stack[-3],\
                'COLS':self.the_semantic_stack[-1]}
        self.insert_into_symbol_table(self.the_semantic_stack[-4], dict)
        four_tuple = (self.the_semantic_stack[-4],\
                      "FORMAL "+self.the_semantic_stack[-6].upper()+" PARAMETER",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)
    
    #24. fparmlist --> { calltype type var
    def analyze_production_24(self):
        dict = {'NAME':self.the_semantic_stack[-1],\
                'TYPE':self.the_semantic_stack[-2],\
                'SHAPE':'scalar',\
                'CALLTYPE':self.the_semantic_stack[-3]}
        self.insert_into_symbol_table(self.the_semantic_stack[-1], dict)
        four_tuple = (None,"BEGIN PARAMETER LIST",None,None)
        self.print_four_tuple(four_tuple)
        four_tuple = (self.the_semantic_stack[-1],\
                      "FORMAL "+self.the_semantic_stack[-3].upper()+" PARAMETER",\
                      1,\
                      None)
        self.print_four_tuple(four_tuple)
    
    #25. fparmlist --> { calltype type var integer
    def analyze_production_25(self):
        dict = {'NAME':self.the_semantic_stack[-2],\
                'TYPE':self.the_semantic_stack[-3],\
                'SHAPE':'vector',\
                'CALLTYPE':self.the_semantic_stack[-4],\
                'SIZE':self.the_semantic_stack[-1]}
        self.insert_into_symbol_table(self.the_semantic_stack[-2], dict)
        four_tuple = (None,"BEGIN PARAMETER LIST",None,None)
        self.print_four_tuple(four_tuple)
        four_tuple = (self.the_semantic_stack[-2],\
                      "FORMAL "+self.the_semantic_stack[-4].upper()+" PARAMETER",\
                      self.the_semantic_stack[-1],\
                      None)
        self.print_four_tuple(four_tuple)
    
    #26. fparmlist --> { calltype type var integer :: integer
    def analyze_production_26(self):
        dict = {'NAME':self.the_semantic_stack[-4],\
                'TYPE':self.the_semantic_stack[-5],\
                'SHAPE':'matrix',\
                'CALLTYPE':self.the_semantic_stack[-6],\
                'ROWS':self.the_semantic_stack[-3],\
                'COLS':self.the_semantic_stack[-1]}
        self.insert_into_symbol_table(self.the_semantic_stack[-4], dict)
        four_tuple = (None,"BEGIN PARAMETER LIST",None,None)
        self.print_four_tuple(four_tuple)
        four_tuple = (self.the_semantic_stack[-4],\
                      "FORMAL "+self.the_semantic_stack[-6].upper()+" PARAMETER",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)
    
    #27. calltype --> VALUE
    def analyze_production_27(self):
        self.the_semantic_stack[-1] = "value"
    
    #28. calltype --> REFERENCE
    def analyze_production_28(self):
        self.the_semantic_stack[-1] = "reference"
        
    #29. execpart --> exechead statlist END   
    def analyze_production_29(self):        
        pass
    
    #30. exechead --> MAIN
    def analyze_production_30(self):        
        four_tuple = ('MAIN', 'LABEL', None, None)
        self.print_four_tuple(four_tuple)
        
    #31. statlist --> statlist stat
    def analyze_production_31(self):        
        pass
    
    #32. statlist --> stat
    def analyze_production_32(self):        
        pass
    
    #33. stat --> whilestat ;
    def analyze_production_33(self):        
        pass
    
    #34. stat --> ifstat ;
    def analyze_production_34(self):        
        pass
    
    #35. stat --> astat
    def analyze_production_35(self):        
        pass
    
    #36. stat --> inputstat ;
    def analyze_production_36(self):        
        four_tuple = ('scanf', 'ENDINPUTPARAMETERS', None, None)
        self.print_four_tuple(four_tuple)
    
    #37. stat --> outputstat ;
    def analyze_production_37(self):        
        four_tuple = ('printf', 'ENDOUTPUTPARAMETERS', None, None)
        self.print_four_tuple(four_tuple)
    
    #38. stat --> callstat ;
    def analyze_production_38(self):        
        pass
    
    #39. inputstat --> inputstat , var
    def analyze_production_39(self):        
        four_tuple = (None, 'INPUTPARAMETER', self.the_semantic_stack[-1], None)
        self.print_four_tuple(four_tuple)
    
    #40. inputstat --> inputstat , var [ aexpr ]
    def analyze_production_40(self):        
        found_symbol = None
        if(self.check_if_present_in_local_symbol_table(self.the_semantic_stack[-4])):
            found_symbol = self.get_symbol_from_local_symbol_table(self.the_semantic_stack[-4])
            #print "found symbol in local ",found_symbol
        else: 
            if(self.check_if_present_in_global_symbol_table(self.the_semantic_stack[-4])):
                found_symbol = self.global_symbol_table[(self.the_semantic_stack[-4])]
                #print "found symbol in global ",found_symbol
            else:
                print "\t\tERROR:",self.the_semantic_stack[-4]," not found."
                return      
        if (found_symbol):
            if found_symbol['SHAPE'] != 'vector':
                print "\t\tERROR:",self.the_semantic_stack[-4],"is not a vector."
                return 
       
        if (self.check_if_aexpr_is_valid(self.the_semantic_stack[-2]) ):
            pass
        else:    
            #print "aexpr in 92 is not valid"
            print "\t\tERROR:",self.the_semantic_stack[-2],"is not a valid index."
            return
        
        four_tuple = (None, 'INPUTSUBPARAMETER', self.the_semantic_stack[-4], self.the_semantic_stack[-2])
        self.print_four_tuple(four_tuple)
        
    #41. inputstat --> inputstat , var [ aexpr : aexpr ]    
    def analyze_production_41(self):
        found_symbol = None
        if(self.check_if_present_in_local_symbol_table(self.the_semantic_stack[-6])):
            found_symbol = self.get_symbol_from_local_symbol_table(self.the_semantic_stack[-6])
            #print "found symbol in local ",found_symbol
            
        else: 
            if(self.check_if_present_in_global_symbol_table(self.the_semantic_stack[-6])):
                found_symbol = self.global_symbol_table[(self.the_semantic_stack[-6])]
                #print "found symbol in global ",found_symbol

            else:
                print "\t\tERROR:",self.the_semantic_stack[-6]," not found."
                return
                
        if (found_symbol):
            if found_symbol['SHAPE'] != 'matrix':
                print "\t\tERROR:",self.the_semantic_stack[-6],"is not a matrix."
                return 
        
        if (self.check_if_aexpr_is_valid(self.the_semantic_stack[-2]) ):
            pass
        else:    
            print "\t\tERROR:",self.the_semantic_stack[-2],"is not a valid index."
            return 
        if (self.check_if_aexpr_is_valid(self.the_semantic_stack[-4]) ):
            pass
        else:    
            print "\t\tERROR:",self.the_semantic_stack[-4],"is not a valid index."
            return    
        
        prefix = 'I'
            
        four_tuple = (self.get_next_IRN(prefix),\
                      "IMULT",\
                      self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])['COLS'],\
                      self.the_semantic_stack[-4])
        self.print_four_tuple(four_tuple)    
        
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        temp_IRN = self.get_current_IRN(prefix)
        four_tuple = (self.get_next_IRN(prefix),\
                      "IADD",\
                      temp_IRN,\
                      self.the_semantic_stack[-2])
        self.print_four_tuple(four_tuple)    
        
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        
        four_tuple = (None, 'INPUTSUBPARAMETER', self.the_semantic_stack[-6], self.get_current_IRN(prefix))
        self.print_four_tuple(four_tuple)
    
    #42. inputstat --> INPUT string
    def analyze_production_42(self):        
        four_tuple = (None, 'CALL', 'scanf', None)
        self.print_four_tuple(four_tuple)
        four_tuple = (None, 'INPUTPARAMETER', self.the_semantic_stack[-1], None)
        self.print_four_tuple(four_tuple)
        
    #43. outputstat --> outputstat , var
    def analyze_production_43(self):        
        four_tuple = (None, 'OUTPUTPARAMETER', self.the_semantic_stack[-1], None)
        self.print_four_tuple(four_tuple)
    
    #44. outputstat --> outputstat , string
    def analyze_production_44(self):        
        four_tuple = (None, 'OUTPUTPARAMETER', self.the_semantic_stack[-1], None)
        self.print_four_tuple(four_tuple)
        
    #45. outputstat --> outputstat , var [ aexpr ]
    def analyze_production_45(self):        
        found_symbol = None
        if(self.check_if_present_in_local_symbol_table(self.the_semantic_stack[-4])):
            found_symbol = self.get_symbol_from_local_symbol_table(self.the_semantic_stack[-4])
            #print "found symbol in local ",found_symbol
        else: 
            if(self.check_if_present_in_global_symbol_table(self.the_semantic_stack[-4])):
                found_symbol = self.global_symbol_table[(self.the_semantic_stack[-4])]
                #print "found symbol in global ",found_symbol
            else:
                print "\t\tERROR:",self.the_semantic_stack[-4]," not found."
                return      
        if (found_symbol):
            if found_symbol['SHAPE'] != 'vector':
                print "\t\tERROR:",self.the_semantic_stack[-4],"is not a vector."
                return 
       
        if (self.check_if_aexpr_is_valid(self.the_semantic_stack[-2]) ):
            pass
        else:    
            #print "aexpr in 92 is not valid"
            print "\t\tERROR:",self.the_semantic_stack[-2],"is not a valid index."
            return
        
        four_tuple = (None, 'OUTPUTSUBPARAMETER', self.the_semantic_stack[-4], self.the_semantic_stack[-2])
        self.print_four_tuple(four_tuple)
        
    #46. outputstat --> outputstat , var [ aexpr : aexpr ]
    def analyze_production_46(self):
        found_symbol = None
        if(self.check_if_present_in_local_symbol_table(self.the_semantic_stack[-6])):
            found_symbol = self.get_symbol_from_local_symbol_table(self.the_semantic_stack[-6])
            #print "found symbol in local ",found_symbol
            
        else: 
            if(self.check_if_present_in_global_symbol_table(self.the_semantic_stack[-6])):
                found_symbol = self.global_symbol_table[(self.the_semantic_stack[-6])]
                #print "found symbol in global ",found_symbol

            else:
                print "\t\tERROR:",self.the_semantic_stack[-6]," not found."
                return
                
        if (found_symbol):
            if found_symbol['SHAPE'] != 'matrix':
                print "\t\tERROR:",self.the_semantic_stack[-6],"is not a matrix."
                return 
        
        if (self.check_if_aexpr_is_valid(self.the_semantic_stack[-2]) ):
            pass
        else:    
            print "\t\tERROR:",self.the_semantic_stack[-2],"is not a valid index."
            return 
        if (self.check_if_aexpr_is_valid(self.the_semantic_stack[-4]) ):
            pass
        else:    
            print "\t\tERROR:",self.the_semantic_stack[-4],"is not a valid index."
            return    
        
        prefix = 'I'
            
        four_tuple = (self.get_next_IRN(prefix),\
                      "IMULT",\
                      self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])['COLS'],\
                      self.the_semantic_stack[-4])
        self.print_four_tuple(four_tuple)    
        
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        temp_IRN = self.get_current_IRN(prefix)
        four_tuple = (self.get_next_IRN(prefix),\
                      "IADD",\
                      temp_IRN,\
                      self.the_semantic_stack[-2])
        self.print_four_tuple(four_tuple)    
        
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        
        four_tuple = (None, 'OUTPUTSUBPARAMETER', self.the_semantic_stack[-6], self.get_current_IRN(prefix))
        self.print_four_tuple(four_tuple)
    
    #47. outputstat --> OUTPUT string
    def analyze_production_47(self):  
        four_tuple = (None, 'CALL', 'printf', None)
        self.print_four_tuple(four_tuple)
        four_tuple = (None, 'OUTPUTPARAMETER', self.the_semantic_stack[-1], None)
        self.print_four_tuple(four_tuple)
    
    #48. callstat --> callname aparmlist }
    def analyze_production_48(self):
        four_tuple = (self.the_semantic_stack[-3], 'ENDACTUALPARAMETERLIST', None, None)
        self.print_four_tuple(four_tuple)
    
    #49. callstat --> callname
    def analyze_production_49(self):
        four_tuple = (None, 'NOACTUALPARAMETERS', None, None)
        self.print_four_tuple(four_tuple)

    
    #50.  callname  -->  CALL  var  
    def analyze_production_50(self):
        if(self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-1])['TYPE'] == 'procedure'):
            four_tuple = (self.the_semantic_stack[-1],\
                      "CALL",\
                      None,\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[-2] = self.the_semantic_stack[-1]    
        else:
            print "\t\tERROR:"," invalid procedure name"
            return
    
    #51.  aparmlist  -->  aparmlist  ,  calltype  var
    def analyze_production_51(self):  
        #print "production 51"
        found_symbol = self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-1])
        if (found_symbol == None):
            print "\t\tERROR:",self.the_semantic_stack[-1]," does not exist"
            return
        
        call_type = 'R' 
        
        if (self.the_semantic_stack[-2] == 'value'):
            call_type = 'V'
            
    
        four_tuple = (None,\
                      "ACTUAL"+call_type+"PARAMETER",\
                      self.the_semantic_stack[-1],\
                      None)
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1       
     
    #52.  aparmlist  ,  calltype  var  [  aexpr  ]
    def analyze_production_52(self):   
        #print "production 52"
        if(self.get_type(self.the_semantic_stack[-2]) != "I"):
            print "\t\tERROR:"," Invalid index"
            return
    
        call_type = 'R' 
        
        if (self.the_semantic_stack[-5] == 'value'):
            call_type = 'V'           
            
        four_tuple = (None,\
                      "ACTUAL"+call_type+"PARAMETER",\
                      self.the_semantic_stack[-4],\
                      self.the_semantic_stack[-2])
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1   
        
       
    #53.            aparmlist  ,  calltype  var  [  aexpr  :  aexpr  ]  
    def analyze_production_53(self):   
        #print "production 53"
        found_symbol = self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])
        if (found_symbol):
            if found_symbol['SHAPE'] != 'matrix':
                    print "\t\tERROR:",self.the_semantic_stack[-6],"is not a matrix."
                    return 
        else:
            print "\t\tERROR:",self.the_semantic_stack[-6]," does not exist"
            return
            
        if(self.get_type(self.the_semantic_stack[-2]) != "I" or self.get_type(self.the_semantic_stack[-4]) != "I"):
            print "\t\tERROR:"," Invalid index"
            return
            
        prefix = 'I'
        four_tuple = (self.get_next_IRN(prefix),\
                      "IMULT",\
                      self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])['COLS'],\
                      self.the_semantic_stack[-3])
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        temp_IRN = self.get_current_IRN(prefix)
        four_tuple = (self.get_next_IRN(prefix),\
                      "IADD",\
                      temp_IRN,\
                      self.the_semantic_stack[-5])
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1   
        
        call_type = 'R' 
        
        if (self.the_semantic_stack[-7] == 'value'):
            call_type = 'V'
            
        
        four_tuple = (None,\
                      "ACTUAL"+call_type+"PARAMETER",\
                      self.the_semantic_stack[-5],\
                      self.get_current_IRN(prefix))
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1   
        
    #54.                  {  calltype  var
    def analyze_production_54(self):
        #print "production 54"
        found_symbol = self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-1])
        if (found_symbol == None):
            print "\t\tERROR:",self.the_semantic_stack[-1]," does not exist"
            return
        
        call_type = 'R' 
#        print "checking call type ",self.the_semantic_stack[-2]
        if (self.the_semantic_stack[-2] == 'value'):
            call_type = 'V'
            
        four_tuple = (None,\
                        "BEGINACTUALPARAMETERLIST",\
                        None,\
                        None)
        self.print_four_tuple(four_tuple)    
            
        four_tuple = (None,\
                      "ACTUAL"+call_type+"PARAMETER",\
                      self.the_semantic_stack[-1],\
                      None)
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1   
        
       
    #55.                  {  calltype  var  [  aexpr  ]  
    def analyze_production_55(self):
        #print "production 55"
        
        found_symbol = self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-4])
        if (found_symbol):
            if found_symbol['SHAPE'] != 'vector':
                    print "\t\tERROR:",self.the_semantic_stack[-6],"is not a vector."
                    return 
        else:
            print "\t\tERROR:",self.the_semantic_stack[-6]," does not exist"
            return
            
        
        if(self.get_type(self.the_semantic_stack[-2]) != "I"):
            print "\t\tERROR:"," Invalid index"
            return
    
        call_type = 'R' 
        
        if (self.the_semantic_stack[-5] == 'value'):
            call_type = 'V'
            
        four_tuple = (None,\
                        "BEGINACTUALPARAMETERLIST",\
                        None,\
                        None)
        self.print_four_tuple(four_tuple)    
            
            
        four_tuple = (None,\
                      "ACTUAL"+call_type+"PARAMETER",\
                      self.the_semantic_stack[-4],\
                      self.the_semantic_stack[-2])
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1   
        
            
 
 
    #56.                  {  calltype  var  [  aexpr  :  aexpr  ]  
    def analyze_production_56(self):
        #print "production 56"
        found_symbol = self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])
        if (found_symbol):
            if found_symbol['SHAPE'] != 'matrix':
                    print "\t\tERROR:",self.the_semantic_stack[-6],"is not a matrix."
                    return 
        else:
            print "\t\tERROR:",self.the_semantic_stack[-6]," does not exist"
            return
            
        if(self.get_type(self.the_semantic_stack[-2]) != "I" or self.get_type(self.the_semantic_stack[-4]) != "I"):
            print "\t\tERROR:"," Invalid index"
            return
            
        four_tuple = (None,\
                        "BEGINACTUALPARAMETERLIST",\
                        None,\
                        None)
        self.print_four_tuple(four_tuple)    
        
        prefix = 'I'
        four_tuple = (self.get_next_IRN(prefix),\
                      "IMULT",\
                      self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])['COLS'],\
                      self.the_semantic_stack[-3])
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        temp_IRN = self.get_current_IRN(prefix)
        four_tuple = (self.get_next_IRN(prefix),\
                      "IADD",\
                      temp_IRN,\
                      self.the_semantic_stack[-5])
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1   
        
        call_type = 'R' 
        
        if (self.the_semantic_stack[-7] == 'value'):
            call_type = 'V'
            
        
        four_tuple = (None,\
                      "ACTUAL"+call_type+"PARAMETER",\
                      self.the_semantic_stack[-5],\
                      self.get_current_IRN(prefix))
        self.print_four_tuple(four_tuple)    
#        self.integer_IRN_counter =  self.integer_IRN_counter+1   
        
     
    #57.  ifstat  -->  ifhead  statlist  END
    def analyze_production_57(self): 
        four_tuple = (self.loop_stack.pop(),"LABEL",None,None)
        self.print_four_tuple(four_tuple)     
     
    #58.  ifstat  -->  ifthen  statlist  END
    def analyze_production_58(self):
        four_tuple = (self.loop_stack.pop(),"LABEL",None,None)
        self.print_four_tuple(four_tuple)
    
    #59.  ifthen  -->  ifhead  statlist  ELSE
    def analyze_production_59(self):
        four_tuple = ("L$"+str(self.label_IRN_counter),"JUMP",None,None)
        self.print_four_tuple(four_tuple)
        self.label_IRN_counter = self.label_IRN_counter + 1
        
        four_tuple = (self.loop_stack.pop(),"LABEL",None,None)
        self.print_four_tuple(four_tuple)
        
        self.loop_stack.append("L$"+str(self.label_IRN_counter-1))
        
    #60.  ifhead  -->  IF  (  bexpr  )  THEN
    def analyze_production_60(self):
        if self.get_type(self.the_semantic_stack[-3]) == 'B':
            four_tuple = ("L$"+str(self.label_IRN_counter),"CJUMP",\
                          self.get_current_IRN('B'),None)
            self.print_four_tuple(four_tuple) 
            self.loop_stack.append("L$"+str(self.label_IRN_counter))
            self.label_IRN_counter = self.label_IRN_counter + 1 
                        
            #self.integer_IRN_counter = self.integer_IRN_counter + 1
        else: 
            print "\t\tERROR:"," In IF, expression is not boolean."

    #61.  whilestat  -->  whileexpr  statlist  END
    def analyze_production_61(self):        
        if len(self.loop_stack) > 1:
            four_tuple = (self.loop_stack.pop(-2),"JUMP",None,None)
            self.print_four_tuple(four_tuple)
        if len(self.loop_stack) > 0:
            four_tuple = (self.loop_stack.pop(),"LABEL",None,None)
            self.print_four_tuple(four_tuple)
    
    #62. whileexpr --> whilehd ( bexpr ) DO
    def analyze_production_62(self):        
        if self.get_type(self.the_semantic_stack[-3]) == 'B':
            four_tuple = ("L$"+str(self.label_IRN_counter),"CJUMP",\
                          self.get_current_IRN('B'),None)
            self.print_four_tuple(four_tuple) 
            self.loop_stack.append("L$"+str(self.label_IRN_counter))
            self.label_IRN_counter = self.label_IRN_counter + 1 
                        
            #self.integer_IRN_counter = self.integer_IRN_counter + 1
        else: 
            print "\t\tERROR:"," In WHILE, expression is not boolean."    

    #63. whilehd --> WHILE
    def analyze_production_63(self):        
        four_tuple = ("L$"+str(self.label_IRN_counter),"LABEL",None,None)
        self.print_four_tuple(four_tuple) 
        self.loop_stack.append("L$"+str(self.label_IRN_counter))
        self.label_IRN_counter = self.label_IRN_counter + 1                
        #self.integer_IRN_counter = self.integer_IRN_counter + 1
    
    #64.  astat  -->  var  <-  astat    
    def analyze_production_64(self):
        x = self.get_type(self.the_semantic_stack[-1])  
        y = self.get_type(self.the_semantic_stack[-3])  
    
        if(x != y):
            four_tuple = (self.get_next_IRN(y),\
                      "CONVERT"+x+"TO"+y,\
                      self.the_semantic_stack[-1],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[-1] = self.get_current_IRN(y)
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
    
        four_tuple = (self.the_semantic_stack[-3],\
                      y+"ASSIGN",\
                      self.the_semantic_stack[-1],\
                      None)
        self.print_four_tuple(four_tuple)    
        #self.the_semantic_stack[-6] = prefix+"$"+str( self.integer_IRN_counter)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1        
        self.the_semantic_stack[-3] = self.the_semantic_stack[-1]        
    
    #65. var  [  aexpr  ]  <-  astat    
    def analyze_production_65(self):
        if(self.get_type(self.the_semantic_stack[-4]) ==  'I' ):
            #print "aexprs are valid"
            pass
        else:
            print "\t\tERROR:"," Invalid index."
            return
            
        found_symbol = self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])
        if (found_symbol):
            if found_symbol['SHAPE'] != 'vector':
                    print "\t\tERROR:",self.the_semantic_stack[-6],"is not a vector."
                    return 
        else:
            print "\t\tERROR:",self.the_semantic_stack[-6]," does not exist"
            return
             
            
        x = self.get_type(self.the_semantic_stack[-1])  
        y = self.get_type(self.the_semantic_stack[-6])  
        if(x != y):
            four_tuple = (self.get_next_IRN(y),\
                      "CONVERT"+x+"TO"+y,\
                      self.the_semantic_stack[-1],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[-1] = self.get_current_IRN(y)
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
            
        four_tuple = (self.the_semantic_stack[-6],\
                      y+"SUBASSIGN",\
                      self.the_semantic_stack[-1],\
                      self.the_semantic_stack[-4])
        self.print_four_tuple(four_tuple)    
        #self.the_semantic_stack[-6] = prefix+"$"+str( self.integer_IRN_counter)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1        
        self.the_semantic_stack[-6] = self.the_semantic_stack[-1]                
        
    #66. var  [  aexpr  :  aexpr  ]  <-  astat
    def analyze_production_66(self):
        if((self.get_type(self.the_semantic_stack[-4]) == 'I') and (self.get_type(self.the_semantic_stack[-6]) == 'I') ):
            #print "aexprs are valid"
            pass
        else:
            print "\t\tERROR:"," Invalid index."
            return
            
        x = self.get_type(self.the_semantic_stack[-1])  
        y = self.get_type(self.the_semantic_stack[-8])  
        if(x != y):
            four_tuple = (self.get_next_IRN(y),\
                      "CONVERT"+x+"TO"+y,\
                      self.the_semantic_stack[-1],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[-1] = self.get_current_IRN(y)
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
            
        prefix = y
            
        four_tuple = (self.get_next_IRN(prefix),\
                      "IMULT",\
                      self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-9])['COLS'],\
                      self.the_semantic_stack[-6])
        self.print_four_tuple(four_tuple)            
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        temp_IRN = self.get_current_IRN(prefix)
        four_tuple = (self.get_next_IRN(prefix),\
                      "IADD",\
                      temp_IRN,\
                      self.the_semantic_stack[-4])
        self.print_four_tuple(four_tuple)    
        
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        
        four_tuple = (self.the_semantic_stack[-8],\
                      prefix+"SUBASSIGN",\
                      self.the_semantic_stack[-1],\
                      self.get_current_IRN(prefix))
        self.print_four_tuple(four_tuple)    
        #self.the_semantic_stack[-6] = prefix+"$"+str( self.integer_IRN_counter)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1        
        self.the_semantic_stack[-8] = self.the_semantic_stack[-1]        
        
    #67.              var  <-  aexpr  ;   
    def analyze_production_67(self):
        x = self.get_type(self.the_semantic_stack[-2])  
        y = self.get_type(self.the_semantic_stack[-4])  
    
        if(x != y):
            four_tuple = (self.get_next_IRN(y),\
                      "CONVERT"+x+"TO"+y,\
                      self.the_semantic_stack[-2],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[-2] = self.get_current_IRN(y)
            #self.loop_stack.append("L$"+str(self.label_IRN_counter))
    
        four_tuple = (self.the_semantic_stack[-4],\
                      y+"ASSIGN",\
                      self.the_semantic_stack[-2],\
                      None)
        self.print_four_tuple(four_tuple)
        #self.the_semantic_stack[-6] = prefix+"$"+str( self.integer_IRN_counter)
        #self.label_IRN_counter =  self.label_IRN_counter + 1        
        self.the_semantic_stack[-4] = self.the_semantic_stack[-2]            
    
    #68. var  [  aexpr  ]  <-  aexpr  ;  
    def analyze_production_68(self):        
        if(self.get_type(self.the_semantic_stack[-5]) ==  'I' ):
            #print "aexprs are valid"
            pass
        else:
            print "\t\tERROR:"," Invalid index."
            return
            
        x = self.get_type(self.the_semantic_stack[-2])  
        y = self.get_type(self.the_semantic_stack[-7])  
        if(x != y):
            four_tuple = (self.get_next_IRN(y),\
                      "CONVERT"+x+"TO"+y,\
                      self.the_semantic_stack[-2],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[-2] = self.get_current_IRN(y)
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
            
        four_tuple = (self.the_semantic_stack[-7],\
                      y+"SUBASSIGN",\
                      self.the_semantic_stack[-2],\
                      self.the_semantic_stack[-5])
        self.print_four_tuple(four_tuple)    
        #self.the_semantic_stack[-6] = prefix+"$"+str( self.integer_IRN_counter)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1        
        self.the_semantic_stack[-7] = self.the_semantic_stack[-2]            
        
    #69. var  [  aexpr  :  aexpr  ]  <-  aexpr  ;   
    def analyze_production_69(self):
        #print "production 69"
        #print "aexpr1 = ",self.the_semantic_stack[-5], " aexpr2 = ",self.the_semantic_stack[-7]," and aexpr3 3= ",self.the_semantic_stack[-2]
        if(self.check_if_aexpr_is_valid(self.the_semantic_stack[-5]) and self.check_if_aexpr_is_valid(self.the_semantic_stack[-7]) ):
            #print "aexprs are valid"
            pass
        else:
            print "\t\tERROR:"," Invalid index."
            return
            
        x = self.get_type(self.the_semantic_stack[-2])  
        y = self.get_type(self.the_semantic_stack[-9])  
        if(x != y):
            four_tuple = (self.get_next_IRN(y),\
                      "CONVERT"+x+"TO"+y,\
                      self.the_semantic_stack[-2],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[-2] = self.get_current_IRN(y)
#            self.integer_IRN_counter =  self.integer_IRN_counter+1            
        prefix = y            
        four_tuple = (self.get_next_IRN(prefix),\
                      "IMULT",\
                      self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-9])['COLS'],\
                      self.the_semantic_stack[-7])
        self.print_four_tuple(four_tuple)
        
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        temp_IRN = self.get_current_IRN(prefix)
        four_tuple = (self.get_next_IRN(prefix),\
                      "IADD",\
                      temp_IRN,\
                      self.the_semantic_stack[-5])
        self.print_four_tuple(four_tuple)    
        
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        
        four_tuple = (self.the_semantic_stack[-9],\
                      prefix+"SUBASSIGN",\
                      self.the_semantic_stack[-2],\
                      self.get_current_IRN(prefix))
        self.print_four_tuple(four_tuple)    
        #self.the_semantic_stack[-6] = prefix+"$"+str( self.integer_IRN_counter)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1        
        self.the_semantic_stack[-9] = self.the_semantic_stack[-2]
    
    #70. notexpr  -->  andexpr & andexpr 
    def analyze_production_70(self):
        if(self.get_type(self.the_semantic_stack[-1])=="B" and self.get_type(self.the_semantic_stack[-3])=="B"):
            four_tuple = (self.get_next_IRN('B'),\
                      "OR",\
                      self.the_semantic_stack[-1],\
                      self.the_semantic_stack[-3])
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[-3] = self.get_current_IRN('B')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1     
        else:
            print "\t\tERROR:",self.the_semantic_stack[-1]," or ",self.the_semantic_stack[-3]," is not boolean."
            return   
   
    #71. notexpr  -->  andexpr & andexpr 
    def analyze_production_71(self):
        pass
   
    #72. notexpr  -->  andexpr & andexpr 
    def analyze_production_72(self):
        if(self.get_type(self.the_semantic_stack[-1])=="B" and self.get_type(self.the_semantic_stack[-3])=="B"):
            four_tuple = (self.get_next_IRN('B'),\
                      "AND",\
                      self.the_semantic_stack[-1],\
                      self.the_semantic_stack[-3])
            self.print_four_tuple(four_tuple)   
            self.the_semantic_stack[-3] = self.get_current_IRN('B')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1     
        else:
            print "\t\tERROR:",self.the_semantic_stack[-1]," or ",self.the_semantic_stack[-3]," is not boolean."
            return
        
    #73. notexpr  -->  andexpr & andexpr 
    def analyze_production_73(self):
        pass
   
    #74. notexpr  -->  ! relexpr  
    def analyze_production_74(self):
        if(self.get_type(self.the_semantic_stack[-1])=="B"):
            four_tuple = (self.get_next_IRN('B'),\
                      "NOT",\
                      self.the_semantic_stack[-1],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[-2] = self.get_current_IRN('B')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1     
        else:
            print "\t\tERROR:",self.the_semantic_stack[-1]," is not boolean."
   
    #75. notexpr  -->  relexpr  
    def analyze_production_75(self):
        pass
   
    #76.relexpr  -->  aexpr  <  aexpr  
    def analyze_production_76(self):
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]

        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            prefix = 'R'
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_current_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'
            
        four_tuple = (self.get_next_IRN('B'),\
                      prefix+"LT",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-3] = self.get_current_IRN('B')
#        self.integer_IRN_counter =  self.integer_IRN_counter+1   
   
    #77.relexpr  -->  aexpr  <=  aexpr  
    def analyze_production_77(self):
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]

        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            prefix = 'R'
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_current_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'
            
        four_tuple = (self.get_next_IRN('B'),\
                      prefix+"LE",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-3] = self.get_current_IRN('B')
#        self.integer_IRN_counter =  self.integer_IRN_counter+1   
   
    #78.relexpr  -->  aexpr  >  aexpr  
    def analyze_production_78(self):
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]

        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            prefix = 'R'
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_current_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'
            
        four_tuple = (self.get_next_IRN('B'),\
                      prefix+"GT",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-3] = self.get_current_IRN('B')
#        self.integer_IRN_counter =  self.integer_IRN_counter+1      
   
    #79.relexpr  -->  aexpr  >=  aexpr  
    def analyze_production_79(self):
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]

        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            prefix = 'R'
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_current_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'
            
        four_tuple = (self.get_next_IRN('B'),\
                      prefix+"GE",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-3] = self.get_current_IRN('B')
#        self.integer_IRN_counter =  self.integer_IRN_counter+1      
    
    #80.relexpr  -->  aexpr  ==  aexpr  
    def analyze_production_80(self):
        
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]

        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            prefix = 'R'
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_current_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'
            
        four_tuple = (self.get_next_IRN('B'),\
                      prefix+"EQ",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-3] = self.get_current_IRN('B')
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
    
    #81.relexpr  -->   aexpr  !=  aexpr     
    def analyze_production_81(self):
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]

        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            prefix = 'R'
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_current_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'
            
        four_tuple = (self.get_next_IRN('B'),\
                      prefix+"NE",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-3] = self.get_current_IRN('B')
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
    
    #82.relexpr  -->  aexpr     
    def analyze_production_82(self):
        pass
    
    #83.  aexpr  -->  aexpr  +  term   
    def analyze_production_83(self):
        #print "prod 83"
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]

        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            prefix = 'R'
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_current_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'
            
            
            
        four_tuple = (self.get_next_IRN(prefix),\
                      prefix+"ADD",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)
        self.the_semantic_stack[-3] = self.get_current_IRN(prefix)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        
    # 84. aexpr  -  term  
    def analyze_production_84(self):
        #print "prod 84"
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]
        #print self.the_semantic_stack
    
        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            prefix = 'R'
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_current_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'
            
            
            
        four_tuple = (self.get_next_IRN(prefix),\
                      prefix+"SUB",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-3] = self.get_current_IRN(prefix)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1

    #85.              -  term  
    def analyze_production_85(self):
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]
        #print "prod 85"   
        prefix = self.get_type(self.the_semantic_stack[-1])
            
        four_tuple = (self.get_next_IRN(prefix),\
                      prefix+"SUB",\
                        0,\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-2] = self.get_current_IRN(prefix)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        
    #86.              term  
    def analyze_production_86(self):
        pass
    
    def get_type(self, term):
        
        if term[0].isdigit():
            if '.' in term:
                return 'R'
            else:
                return 'I'
        elif '$' in term:
            return term[0]
        elif  (self.get_symbol_from_global_or_local_symbol_table(term)):
            x = self.get_symbol_from_global_or_local_symbol_table(term)
            return x['TYPE'][0].upper()
        else:
            try:
                int(term)
            except Exception:
                print term, "does not have a type "
                return 
            return 'I'
             #print self.the_semantic_stack[i]
        print term, "does not have a type "
        return  
        pass
    
    def check_if_in_mix_arithmatic_mode(self, term1, term2):
        x = self.get_type(term1)
        y = self.get_type(term2)
       
        #print "type of ",term1," is ",x," and type of ",term2, " is ",y
       
        if x == y:
            return False
        else:
            return True
        
    #87.  term  -->  term  *  primary
    def analyze_production_87(self):
        #print self.the_semantic_stack
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]
        prefix = 'R'
        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_next_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'
            
        four_tuple = (self.get_next_IRN(prefix),\
                      prefix+"MULT",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-3] = self.get_current_IRN(prefix)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        #print self.the_semantic_stack
   
    #88.  term  -->  term  /  primary
    def analyze_production_88(self):
        #print self.the_semantic_stack
        #print "term = ",self.the_semantic_stack[-3], " primary = ",self.the_semantic_stack[-1]
        prefix = 'R'

        if(self.check_if_in_mix_arithmatic_mode(self.the_semantic_stack[-3],self.the_semantic_stack[-1])):
            
            prefix = 'R'
            index_of_term_to_convert = 11
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                #print "convert ",self.the_semantic_stack[-1]," to real"
                index_of_term_to_convert = -1
            else:
                #print "convert ",self.the_semantic_stack[-3]," to real"
                index_of_term_to_convert = -3
            
            four_tuple = (self.get_next_IRN('R'),\
                      "CONVERTITOR",\
                      self.the_semantic_stack[index_of_term_to_convert],\
                      None)
            self.print_four_tuple(four_tuple)    
            self.the_semantic_stack[index_of_term_to_convert] = self.get_current_IRN('R')
#            self.integer_IRN_counter =  self.integer_IRN_counter+1
        else:
            if(self.get_type(self.the_semantic_stack[-3])=="R"):
                prefix = 'R'
            else:
                prefix = 'I'                        
            
        four_tuple = (self.get_next_IRN(prefix),\
                      prefix+"DIV",\
                      self.the_semantic_stack[-3],\
                      self.the_semantic_stack[-1])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-3] = self.get_current_IRN(prefix)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        #print self.the_semantic_stack
   
    #89.  term  -->  primary\00\00
    def analyze_production_89(self):
        pass

    #90.  primary  -->  (  bexpr  )
    def analyze_production_90(self):
        #print "putting ",self.the_semantic_stack[-2], " at the place of ",self.the_semantic_stack[-3] 
        #print self.the_semantic_stack
        self.the_semantic_stack[-3] = self.the_semantic_stack[-2]
        #print self.the_semantic_stack
    
    
    
    def check_if_present_in_local_symbol_table(self,key):
        if(self.in_procedure != 'GLOBAL' and self.local_symbol_table[self.in_procedure][-1].has_key(key)):
            return True
        else:
            return False
        
        
    def check_if_present_in_global_symbol_table(self,key):
        if(self.global_symbol_table.has_key(key)):
            return True
        else:
            return False
            
    def get_symbol_from_local_symbol_table(self,key):
        return self.local_symbol_table[self.in_procedure][-1][key]
    
    def get_symbol_from_global_symbol_table(self,key):
        return self.global_symbol_table[key]
        
    def get_symbol_from_global_or_local_symbol_table(self,key):
        if(self.check_if_present_in_local_symbol_table(key)):
            return self.get_symbol_from_local_symbol_table(key)
        else: 
            if(self.check_if_present_in_global_symbol_table(key)):
                return self.get_symbol_from_global_symbol_table(key)
            
            else:
                return None
            
    
    def check_if_aexpr_is_valid(self, aexpr):
        if(aexpr.isdigit()):        
            return True
        
        if(aexpr[0] == 'I'):            
            return True

        if(self.check_if_present_in_local_symbol_table(aexpr)):
            if (type(aexpr) is str):
                if(self.get_symbol_from_local_symbol_table(aexpr)['TYPE'] == 'integer'):
                    return True
#                if(aexpr[0] == 'I'):
#                    #print "aexpr is valid string : ",aexpr[0]
#                    return True
#                else:
#                    #print "aexpr is not valid string : ",aexpr[0]
#                    return False
        else:
            if(self.check_if_present_in_global_symbol_table(aexpr)):
                if (type(aexpr) is str):
                    if(self.get_symbol_from_global_symbol_table(aexpr)['TYPE'] == 'integer'):
                        return True
#                    if(aexpr[0] == 'I'):
#                        #print "aexpr is valid string : ",aexpr[0]
#                        return True
#                    else:
#                        #print "aexpr is valid string : ",aexpr[0]
#                
#                        #print "aexpr is not valid string"
#                        return False
            else:                
                print "\t\tERROR:",aexpr," not found."
                return False
        
    
    #91. primary --> var [ aexpr : aexpr ]
    def analyze_production_91(self):  
        
        found_symbol = None
        if(self.check_if_present_in_local_symbol_table(self.the_semantic_stack[-6])):
            found_symbol = self.get_symbol_from_local_symbol_table(self.the_semantic_stack[-6])
            #print "found symbol in local ",found_symbol
            
        else: 
            if(self.check_if_present_in_global_symbol_table(self.the_semantic_stack[-6])):
                found_symbol = self.global_symbol_table[(self.the_semantic_stack[-6])]
                #print "found symbol in global ",found_symbol

            else:
                print "\t\tERROR:",self.the_semantic_stack[-6]," not found."
                return
                
        if (found_symbol):
            if found_symbol['SHAPE'] != 'matrix':
                    print "\t\tERROR:",self.the_semantic_stack[-6],"is not a matrix."
                    return 
        
        if (self.check_if_aexpr_is_valid(self.the_semantic_stack[-2]) ):
            pass
        else:    
            print "\t\tERROR:",self.the_semantic_stack[-2],"is not a valid index."
            return 
        if (self.check_if_aexpr_is_valid(self.the_semantic_stack[-4]) ):
            pass
        else:    
            print "\t\tERROR:",self.the_semantic_stack[-4],"is not a valid index."
            return    
        
        prefix = 'I'
            
        four_tuple = (self.get_next_IRN(prefix),\
                      "IMULT",\
                      self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])['COLS'],\
                      self.the_semantic_stack[-4])
        self.print_four_tuple(four_tuple)    
        
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        temp_IRN = self.get_current_IRN(prefix)
        four_tuple = (self.get_next_IRN(prefix),\
                      "IADD",\
                      temp_IRN,\
                      self.the_semantic_stack[-2])
        self.print_four_tuple(four_tuple)    
        
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        
        if(self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])['TYPE'] == 'integer'):
            prefix = 'I'
        else: 
            if(self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-6])['TYPE'] == 'real'):
                prefix = 'R'
                
        temp_IRN = self.get_current_IRN('I')
        four_tuple = (self.get_next_IRN(prefix),\
                      "SUBLOAD",\
                      self.the_semantic_stack[-6],\
                      temp_IRN)
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-6] = self.get_current_IRN(prefix)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        
        
    #92.  primary  -->  var  [  aexpr  ]
    def analyze_production_92(self):
    
        found_symbol = None
        if(self.check_if_present_in_local_symbol_table(self.the_semantic_stack[-4])):
            found_symbol = self.get_symbol_from_local_symbol_table(self.the_semantic_stack[-4])
#            print "found symbol in local ",found_symbol
        else: 
            if(self.check_if_present_in_global_symbol_table(self.the_semantic_stack[-4])):
                found_symbol = self.global_symbol_table[(self.the_semantic_stack[-4])]
#                print "found symbol in global ",found_symbol
            else:
                print "\t\tERROR:",self.the_semantic_stack[-4]," not found."
                return      
        if (found_symbol):
            if found_symbol['SHAPE'] != 'vector':
                    print "\t\tERROR:",self.the_semantic_stack[-4],"is not a vector."
                    return 
       
        if (self.check_if_aexpr_is_valid(self.the_semantic_stack[-2]) ):
            pass
        else:    
            #print "aexpr in 92 is not valid"
            print "\t\tERROR:",self.the_semantic_stack[-2],"is not a valid index."
            return 
        
        if(self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-4])['TYPE'] == 'integer'):
            prefix = 'I'
        else: 
            if(self.get_symbol_from_global_or_local_symbol_table(self.the_semantic_stack[-4])['TYPE'] == 'real'):
                prefix = 'R'
                
        four_tuple = (self.get_next_IRN(prefix),\
                      "SUBLOAD",\
                      self.the_semantic_stack[-4],\
                      self.the_semantic_stack[-2])
        self.print_four_tuple(four_tuple)    
        self.the_semantic_stack[-4] = self.get_current_IRN(prefix)
#        self.integer_IRN_counter =  self.integer_IRN_counter+1
        
     
    #93.  primary  -->  var
    def analyze_production_93(self):
        pass
     
    #94. primary --> constant
    def analyze_production_94(self):
        pass
        
    #95. constant --> integer
    def analyze_production_95(self):
        pass
    
    #96. constant --> real
    def analyze_production_96(self):
        pass
        
    #29.  execpart  -->  exechead  statlist  END
    def analyze_production_29(self):
        pass
