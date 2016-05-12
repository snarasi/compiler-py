#!/usr/bin/python
import re, sys, string
import Config


class Pragmatic:
    def __init__(self):
        self.out_file_handler = open((Config.file_name.split('.')[0] +".asm"),"w")
        self.registers = {'edi':{'used':False,'variable':False,'IRN':False,'variableName':"",'name':"edi"},'ebx':{'used':False,'variable':False,'IRN':False,'variableName':"",'name':"ebx"},'ecx':{'used':False,'variable':False,'IRN':False,'variableName':"",'name':"ecx"},'esi':{'used':False,'variable':False,'IRN':False,'variableName':"",'name':"esi"}}
        self.memory_segment_started = False
        self.text_segment_started = False
        self.output_string = ""
        self.bss_section_string = ""
        self.is_in_print_call = False
        self.string_counter = 0
        self.print_stack = []
        self.previous_comparison = ""
        self.data_section_string = ""
        self.global_variables = []
        self.in_procedure = ""
        self.procedure_stack = []
        self.parameter_list = []
        self.formal_parameter_list = {}
        self.local_variable_list = {}
        pass
    
    def get_next_string_counter(self):
        self.string_counter = self.string_counter + 1
        return str(self.string_counter - 1)
        
    def add_to_bss_section_string(self,string):
        self.bss_section_string = self.bss_section_string + "\n" + string
    
    def add_to_data_section_string(self,string):
        if self.data_section_string == "":
            self.data_section_string = self.data_section_string+ "segment .data\n"

        self.data_section_string = self.data_section_string + "\n" + string
    
    def is_integer(self,number):
        try:
            int(number)
        except Exception:
            return False
        return True
    
    def print_tuple_generation(self,string):
        print string
    
    def write_to_file(self,string,number_of_tabs):
        tab_string = ""
        for i in range(number_of_tabs):
            tab_string = tab_string +"\t"
#        self.print_tuple_generation(tab_string+string+"\n")
        self.out_file_handler.write(tab_string+string+"\n")
    
    def print_reg_status(self):
        for reg in self.registers.values():
            print reg['name']," and ",reg['variableName']
    
    def get_available_register(self):
        
        for register in self.registers.values():
            if(register['used'] == False):
                return register
        
        for register in self.registers.values():
            if(register['variable'] == True):
                return register

        for register in self.registers.values():
            if(register['used'] == True and register['variable'] == False and register['IRN'] == False):
                return register
        
        print "no registers available !!! error ########"
        
      
    def get_avaiable_register_except(self,used_register):
        for register in self.registers.values():
            if(register['used'] == False and register != used_register):
                return register
                
        for register in self.registers.values():
            if(register['variable'] == True and register != used_register):
                return register
        pass
        
    def get_register_holding_variable(self,variable_name):
        for register in self.registers.values():
            if (register['variableName'] == variable_name):
                return register
    
    def do_pragmatic(self,tuple):
        if self.in_procedure == "":
            if tuple[1] == "MEMORY":   
                self.handle_MEMORY(tuple)
            elif tuple[1] == "LABEL":
                self.handle_LABEL(tuple)
            elif tuple[1] == "IASSIGN":
                self.handle_IASSIGN(tuple)
            elif tuple[1] == "ISUBASSIGN":
                self.handle_ISUBASSIGN(tuple)
            elif tuple[1] == "IADD":
                self.handle_IADD(tuple)
            elif tuple[1] == "ISUB":
                self.handle_ISUB(tuple)
            elif tuple[1] == "IMULT":
                self.handle_IMULT(tuple)
            elif tuple[1] == "CALL":    
                self.handle_CALL(tuple)
            elif tuple[1] == "OUTPUTPARAMETER":    
                self.handle_OUTPUTPARAMETER(tuple)    
            elif tuple[1] == "OUTPUTSUBPARAMETER":    
                self.handle_OUTPUTSUBPARAMETER(tuple) 
            elif tuple[1] == "ENDOUTPUTPARAMETERS":    
                self.handle_ENDOUTPUTPARAMETERS(tuple)
            elif tuple[1] == "SUBLOAD":    
                self.handle_SUBLOAD(tuple) 
            elif tuple[1] == "ILT":    
                self.handle_ILT(tuple) 
            elif tuple[1] == "IGT":    
                self.handle_IGT(tuple)
            elif tuple[1] == "IGE":    
                self.handle_IGE(tuple)    
            elif tuple[1] == "IEQ":    
                self.handle_IEQ(tuple)          
            elif tuple[1] == "CJUMP":    
                self.handle_CJUMP(tuple) 
            elif tuple[1] == "JUMP":    
                self.handle_JUMP(tuple)
            elif tuple[1] == "BEGIN PROCEDURE":
                self.handle_PROCEDURE(tuple)                
        else:    
            self.handle_PROCEDURE(tuple)
        
        pass
    
    def set_parameters_to_register(self,register,is_used,is_variable,is_irn,variable_name):
        if not is_used and not is_variable and not is_irn and variable_name == "":
            pass
        
        register['used'] = is_used
        register['variable'] = is_variable
        register['IRN'] = is_irn
        register['variableName'] = variable_name
     
   
    def handle_MEMORY(self,tuple):
        if not self.in_procedure:
            if not self.memory_segment_started:
                self.add_to_bss_section_string("segment .bss\n")
                self.memory_segment_started = True
            if tuple[3] == None:
                self.output_string = tuple[0]+" "+"resd "+str(tuple[2])
            else:
                self.output_string = tuple[0]+" resd "+str(int(tuple[2])*int(tuple[3])) 
            
            self.global_variables.append(tuple[0])    
            self.add_to_bss_section_string(self.output_string)
        else:
            self.write_to_file('sub esp, 4', 1)
            self.local_variable_list[tuple[0]] = 'ebp-'+str(len(self.local_variable_list)*4+4)
            
    def handle_LABEL(self,tuple):                
        if tuple[0] == "MAIN":
            if not self.text_segment_started:
                self.write_to_file("\nsegment .text",0)
                self.text_segment_started = True
            self.output_string = "global  "+"main\n"
            self.write_to_file(self.output_string,1)
            self.write_to_file("main:\nenter 0,0\npusha",0)
        else:
            self.write_to_file(tuple[0]+":",0)
        pass
        
    def handle_IASSIGN(self, tuple):
        if '$' in tuple[2]:
            register = self.get_register_holding_variable(tuple[2])
            if self.is_integer(tuple[0]):
                self.write_to_file("mov "+tuple[0]+" , "+register['name'] , 1)
                self.set_register_free(register )

            else:
                self.write_to_file("mov "+"["+tuple[0]+"], "+register['name'] , 1)
                self.set_register_free(register)

        elif tuple[3] == None:
            self.write_to_file("mov dword ["+tuple[0]+"], "+ tuple[2] , 1)
            pass    
    
    def handle_ISUBASSIGN(self, tuple):
        if  self.is_integer(tuple[3]) and self.is_integer(tuple[2]) :
            self.write_to_file("mov dword ["+tuple[0]+" + "+tuple[3]+"*4"+"], "+tuple[2] ,1 )
    
        elif '$' in tuple[3] and '$' not in tuple[2] :
            register1 = self.get_available_register()
            self.handle_register_parameters(register1, tuple[0])
            if self.is_integer(tuple[2]):
                register2 = self.get_register_holding_variable(tuple[3])
                self.write_to_file("mov "+ "dword ["+tuple[0]+"+"+ str(register2['name']+"*4") +"], "+tuple[2], 1 )
                self.set_parameters_to_register(register2,False, False, False,"" )  
            else: 
                register2 = self.get_register_holding_variable(tuple[3])
                self.write_to_file("mov "+ " ["+tuple[0]+"+"+ str(register2['name']+"*4") +"], ["+tuple[2]+"]", 1 )
                self.set_parameters_to_register(register2,False, False, False,"" )
        
        elif '$' in tuple[3] and '$'  in tuple[2] :
            register1 = self.get_register_holding_variable(tuple[2])
            register2 = self.get_register_holding_variable(tuple[3])
            self.write_to_file("mov "+ " ["+tuple[0]+"+"+ str(register2['name']+"*4") +"],"+ register1['name'], 1 )
            self.set_parameters_to_register(register2,False, False, False,"" )
            self.handle_register_parameters(register1, tuple[0])
            
        elif self.is_integer(tuple[3]) :
            register1 = self.get_available_register()
            self.write_to_file("mov "+ register1['name']+ ", ["+tuple[0]+"+"+ str(tuple[3])+"*4" +"]", 1 )
            self.set_parameters_to_register(register1,True, False, True,tuple[0] )
        else:
            register1 = self.get_available_register()
            register2 = self.get_register_holding_variable(tuple[3])
            if register2 is not None:
                self.write_to_file("mov "+ "["+tuple[0]+"+"+ str(register2['name']+"*4") +"], "+register1['name'], 1 )
                self.set_parameters_to_register(register1,False, False, False,"" )
                self.set_parameters_to_register(register2,False, False, False,"" )
            else:
                register2 = self.get_available_register()
                self.write_to_file("mov "+ register2['name']+ ", ["+tuple[3] +"]", 1 )
                self.set_parameters_to_register(register2,True, False, True,tuple[3] )
                if '$' in tuple[2]:
                    register1 = self.get_register_holding_variable(tuple[2])
                    self.write_to_file("mov "+ " ["+tuple[0]+"+"+ str(register2['name']+"*4") +"], "+ register1['name'], 1 )
                    self.set_parameters_to_register(register1,False, False, False,"" )
                    self.set_parameters_to_register(register2,False, False, False,"" )
                else:
                    register1 = self.get_available_register()
                    self.write_to_file("mov "+register1['name'] + ", ["+tuple[2]+"]", 1 )
                    self.write_to_file("mov "+ " ["+tuple[0]+"+"+ str(register2['name']+"*4") +"], "+register1['name'], 1 )
                    self.set_parameters_to_register(register1,False, False, False,"" )
                    self.set_parameters_to_register(register2,False, False, False,"" )
                    pass    
            
    def handle_IADD(self, tuple):
        self.handle_function(tuple,"add")
        pass
        
    def handle_ISUB(self, tuple):
        self.handle_function(tuple,"sub")
        pass
    
    def handle_IMULT(self, tuple):    
        second_argument = self.handle_second_oprand(tuple[3])
        if self.is_integer(tuple[2]):
            self.write_to_file('mov eax, '+tuple[2], 1)
        elif '$' not in tuple[2]:
            self.write_to_file('mov eax, ['+tuple[2]+']', 1)
        else:
            register =  self.get_register_holding_variable(tuple[2])
            self.write_to_file('mov eax, '+register['name'], 1)
            self.set_register_free(register)
           
        self.write_to_file('imul eax, '+second_argument, 1)
        register = self.get_available_register()
        self.write_to_file('mov '+register['name']+', eax', 1)
        self.handle_register_parameters(register, tuple[0])

        if self.registers.has_key(second_argument) and second_argument != "":
             self.set_register_free(self.registers[second_argument])
    
    def handle_first_oprand(self,opr):
        first_argument = ""
        if opr is not None:
            if '$' in opr:
                register1 =  self.get_register_holding_variable(opr)      
                first_argument = register1['name']
            else:
                if self.get_register_holding_variable(opr) is not None:
                    first_argument = self.get_register_holding_variable(opr)['name']
                    
                elif self.is_integer(opr) :
                    register1 = self.get_available_register()
                    self.write_to_file("mov "+register1['name']+", "+opr , 1)
                    self.set_parameters_to_register(register1,True, False, False,opr )    
                    first_argument = register1['name']
                elif opr in self.global_variables :
                    register1 = self.get_available_register()
                    self.write_to_file("mov "+register1['name']+", ["+opr+"]" , 1)
                    self.set_parameters_to_register(register1,True, False, False,opr )    
                    first_argument = register1['name']                
                else:
                    register1 = self.get_available_register()
                    self.write_to_file("mov "+register1['name']+", "+opr , 1)
                    self.set_parameters_to_register(register1,True, True, False,opr )    
                    first_argument = register1['name']    
                    
        return first_argument
    
    def handle_second_oprand(self,opr):
        
        first_argument = ""
        if opr is not None:
            if '$' in opr:
                register1 =  self.get_register_holding_variable(opr)     
                first_argument = register1['name']
            elif self.is_integer(opr) :
                first_argument = opr
            elif opr in self.global_variables :
                first_argument = "["+opr+"]"
            else:
                register1 = self.get_available_register()
                self.write_to_file("mov "+register1['name']+", "+opr , 1)
                self.set_parameters_to_register(register1,True, True, False,opr )    
                first_argument = register1['name']    
        return first_argument
    
    def handle_register_parameters(self,register,tuple_entry):
        if '$' in tuple_entry:
            self.set_parameters_to_register(register,True, False, True,tuple_entry )
        elif self.is_integer(tuple_entry) :
            self.set_parameters_to_register(register,True, False, False,tuple_entry )
        else:
            self.set_parameters_to_register(register,True, True, False,tuple_entry )   
            
    def set_register_free(self,register):
        if register is not None:
            self.set_parameters_to_register(register,False,False,False,"")
            
    def handle_function(self, tuple, function):        
        first_argument = self.handle_first_oprand(tuple[2])
        if self.registers.has_key(first_argument):   
            self.handle_register_parameters(self.registers[first_argument],tuple[0])
            
        second_argument = self.handle_second_oprand(tuple[3])
        string = ""
        if second_argument == "":
            string = function+" "+ first_argument 
        else:
            string = function+" "+ first_argument + ", " + second_argument
        
        self.write_to_file(string , 1)
                
        if self.registers.has_key(second_argument) and second_argument != "":
             self.set_register_free(self.registers[second_argument])   

    def handle_CALL(self, tuple):
        if tuple[2] == "printf":
            self.is_in_print_call = True
            self.write_to_file("extern printf",1)
        elif tuple[2] == None:
            self.procedure_stack.append(self.in_procedure)
            self.in_procedure = tuple[0]
            
    def handle_OUTPUTPARAMETER(self, tuple):
        
        if tuple[2][0] =="\"":
            
            variable_name =  "string"+self.get_next_string_counter()
            string1 = tuple[2]
            string1= string1.replace("\"","`")
            
            string = "string"+str(self.string_counter-1)+"\t"+"db\t"+string1 +", 0"
            self.add_to_data_section_string(string)   
            self.print_stack.append("push "+variable_name+"")
        
        else:
            if '$' in tuple[2]:
                register1 = self.get_register_holding_variable(tuple[2])
                self.print_stack.append("push "+register1['name'])
            else:
                register1 = self.get_available_register()   
                if self.is_integer(tuple[2]) :
                    register1 = self.get_available_register()   
                    self.write_to_file("mov "+ register1['name']+ ", "+tuple[2]+"", 1 )
                    self.set_parameters_to_register(register1,True, False, False,tuple[2] )
                    self.print_stack.append("push "+register1['name'])
                else:
                    self.write_to_file("mov "+ register1['name']+ ", ["+tuple[2]+"]", 1 )
                    self.set_parameters_to_register(register1,True, True, False,tuple[2] )
                    self.print_stack.append("push "+register1['name'])                                
        pass
        
    def handle_OUTPUTSUBPARAMETER(self,tuple):
#        self.print_reg_status()
        if tuple[3] is None:
            pass    
        else:

            if self.is_integer(tuple[3]) :
                register1 = self.get_available_register()   
                self.write_to_file("mov "+ register1['name']+ ", ["+tuple[2]+"+"+ str(int(tuple[3])*4) +"]", 1 )
                self.set_parameters_to_register(register1,True, False, False,tuple[2] )
                self.print_stack.append("push "+register1['name'])

            else:
                register1 = self.get_available_register()
                register2 = self.get_register_holding_variable(tuple[3])
                if register2 is not None:
                    if self.is_integer(tuple[2]):
                        self.write_to_file("mov "+ register1['name']+ ", ["+tuple[2]+"+"+ str(tuple[3]+"*4") +"]", 1 )
                        self.set_parameters_to_register(register1,True, False, False,tuple[2] )
                        self.print_stack.append("push "+register1['name'])
                    elif tuple[2] in self.global_variables:
                        register1 = self.get_available_register()
                        self.write_to_file("mov "+ register1['name']+ ", ["+tuple[2]+"+"+ register2['name']+"*4" +"]", 1 )
                        self.set_register_free(register2)
                        self.set_parameters_to_register(register1,True, False, False,tuple[3] )
                        self.print_stack.append("push "+register1['name'])
                    else:
                        self.write_to_file("mov "+register1['name']+", "+register2['name']  , 1)
                        self.set_register_free(register2)
                        self.set_parameters_to_register(register1,True, True, False,tuple[3] )   
                        self.print_stack.append("push "+register1['name'])                                                    
                else:
                    register2 = self.get_available_register()           
                    self.write_to_file("mov "+ register2['name']+ ", ["+ tuple[3] +"]", 1 )
                    self.set_parameters_to_register(register2,True, True, False,tuple[3] )
                    register1 = self.get_available_register()   
                    self.write_to_file("mov "+ register1['name']+ ", ["+tuple[2]+"+"+ register2['name']+"*4" +"]", 1 )
                    self.print_stack.append("push "+register1['name'])		
                    self.set_parameters_to_register(register2,False, False, False,"" )
                    self.set_parameters_to_register(register1,True, False, False,tuple[2] )
                                    
    def handle_ENDOUTPUTPARAMETERS(self,tuple):
        
        counter = 0
        for i in range(len(self.print_stack)):
            counter = counter + 1
            string = self.print_stack.pop()
            self.write_to_file(string,1)
              
            if self.registers.has_key(string.split(' ')[1]):
                self.set_parameters_to_register(self.registers[string.split(' ')[1]],False,False,False,"")
        
        self.write_to_file("call printf",1)
        self.write_to_file("add esp,"+str(counter*4),1)
        pass
   
   
    def handle_SUBLOAD(self,tuple):
#        self.print_reg_status()
        if '$' in tuple[3]:
            register1 = self.get_available_register()
            self.set_parameters_to_register(register1,True, False, True,tuple[0] )
            register2 = self.get_register_holding_variable(tuple[3])
            self.write_to_file("mov "+ register1['name']+ ",  ["+tuple[2]+"+"+ str(register2['name']+"*4") +"]", 1 )
            self.set_parameters_to_register(register2,False, False, False,"" )

        elif self.is_integer(tuple[3]) :
            register1 = self.get_available_register()
            self.write_to_file("mov "+ register1['name']+ ", ["+tuple[2]+"+"+ str(tuple[3])+"*4" +"]", 1 )
            self.set_parameters_to_register(register1,True, False, True,tuple[0] )
        else:
            register1 = self.get_available_register()
            register2 = self.get_register_holding_variable(tuple[3])
            if register2 is not None:
                self.write_to_file("mov "+ register1['name']+ ", ["+tuple[2]+"+"+ str(register2['name']+"*4") +"]", 1 )
                self.set_parameters_to_register(register1,True, False, True,tuple[0] )
                self.set_parameters_to_register(register2,False, False, False,"" )
            else:
                register2 = self.get_available_register()
                self.write_to_file("mov "+ register2['name']+ ", ["+tuple[3] +"]", 1 )
                self.set_parameters_to_register(register1,True, False, True,tuple[3] )
                register1 = self.get_available_register()
                self.write_to_file("mov "+ register1['name']+ ", ["+tuple[2]+"+"+ str(register2['name']+"*4") +"]", 1 )
                self.set_parameters_to_register(register1,True, False, True,tuple[0] )
                self.set_register_free(register2)
        
    def handle_ILT(self,tuple):
        self.previous_comparison = "ILT"
        self.handle_function(tuple,"cmp")
        
    def handle_IGT(self,tuple):
        self.previous_comparison = "IGT"    
        self.handle_function(tuple,"cmp")
        
    def handle_IGE(self,tuple):
        self.previous_comparison = "IGE"    
        self.handle_function(tuple,"cmp")

    def handle_IEQ(self,tuple):
        self.previous_comparison = "IEQ"    
        self.handle_function(tuple,"cmp")
   
    def handle_CJUMP(self,tuple):
        if self.previous_comparison == "IEQ":
            self.write_to_file("jne "+ tuple[0], 1 )
            self.set_register_free(self.get_register_holding_variable(tuple[2]))
        elif   self.previous_comparison == "IGT":
            self.write_to_file("jng "+ tuple[0], 1 )
            self.set_register_free(self.get_register_holding_variable(tuple[2]))
        elif   self.previous_comparison == "IGE":
            self.write_to_file("jl "+ tuple[0], 1 )
            self.set_register_free(self.get_register_holding_variable(tuple[2]))
        elif   self.previous_comparison == "ILT":
            self.write_to_file("jnl "+ tuple[0], 1 )
            self.set_register_free(self.get_register_holding_variable(tuple[2]))
        
    def handle_JUMP(self,tuple):
        self.write_to_file("JMP "+ tuple[0], 1 )

    def handle_PROCEDURE(self,tuple):
        if tuple[1] == "BEGIN PROCEDURE":
            self.in_procedure = tuple[0]
            self.write_to_file(tuple[0]+':', 0)
            self.write_to_file('push ebp', 1)
            self.write_to_file('mov ebp, esp', 1)
        elif tuple[1] == "BEGIN PARAMETER LIST":
            self.formal_parameter_list.clear()
        elif tuple[1] == "FORMAL VALUE PARAMETER":
            self.formal_parameter_list[tuple[0]] = {'address':'ebp+'+str(len(self.formal_parameter_list)*4+8),'type':'VAL'}
        elif tuple[1] == "FORMAL REFERENCE PARAMETER":
            self.formal_parameter_list[tuple[0]] = {'address':'ebp+'+str(len(self.formal_parameter_list)*4+8),'type':'REF'}
        elif tuple[1] == "END PARAMETER LIST":
            pass             
        elif tuple[1] == "IASSIGN":            
            if '$' in tuple[2]:
                print "$ found in tuple : ",tuple
                register = self.get_register_holding_variable(tuple[2])
                print "register holding variable : ",register['name']
                if self.is_integer(tuple[0]):
                    self.write_to_file("mov "+tuple[0]+" , "+register['name'] , 1)
                    self.set_parameters_to_register(register,False, False, False,"" )
    
                else:
                    if self.formal_parameter_list.has_key(tuple[0]):
                        self.write_to_file("mov "+"["+self.formal_parameter_list[tuple[0]]['address']+"], "+register['name'] , 1)
                    elif self.local_variable_list.has_key(tuple[0]):
                        self.write_to_file("mov "+"["+self.local_variable_list[tuple[0]]+"], "+register['name'] , 1)                    
                    else:
                        self.write_to_file("mov "+"["+tuple[0]+"], "+register['name'] , 1)
                    self.set_parameters_to_register(register,False, False, False,"" )
    
            elif tuple[3] == None:                
                if self.local_variable_list.has_key(tuple[0]):
                    self.write_to_file("mov dword ["+self.local_variable_list[tuple[0]]+"], "+ tuple[2] , 1)
                elif self.formal_parameter_list.has_key(tuple[0]):
                    if self.formal_parameter_list[tuple[0]]['type'] == 'REF':
                        register = self.get_available_register()
                        self.write_to_file('mov '+register['name']+', ['+self.formal_parameter_list[tuple[0]]['address']+']', 1)
                        self.handle_register_parameters(register, self.formal_parameter_list[tuple[0]]['address'])
                        self.write_to_file("mov dword ["+register['name']+"], "+ tuple[2] , 1)                        
                    else:
                        self.write_to_file("mov dword ["+self.formal_parameter_list[tuple[0]]['address']+"], "+ tuple[2] , 1)
                else:
                    self.write_to_file("mov dword ["+tuple[0]+"], "+ tuple[2] , 1)     
                pass
        elif tuple[1] == "ISUB":
            newtuple = [tuple[0],tuple[1],'['+self.formal_parameter_list[tuple[2]]['address']+']',tuple[3]]
            self.handle_ISUB(newtuple)
        elif tuple[1] == "IADD":
            if self.formal_parameter_list.has_key(tuple[2]):
                newtuple = [tuple[0],tuple[1],'['+self.formal_parameter_list[tuple[2]]['address']+']',tuple[3]]
            elif self.local_variable_list.has_key(tuple[2]):
                newtuple = [tuple[0],tuple[1],'['+self.local_variable_list[tuple[2]]+']',tuple[3]]
            elif '$' in tuple[2]:
                newtuple = tuple
            else:
                newtuple = [tuple[0],tuple[1],'['+tuple[2]+']',tuple[3]]
            print newtuple                 
            self.handle_IADD(newtuple)
        elif tuple[1] == "IMULT":
            newtuple = [tuple[0],tuple[1],'['+tuple[2]+']',tuple[3]] 
            if self.is_integer(tuple[2]) or '$' in tuple[2]:
                newtuple[2] = tuple[2]
            elif self.formal_parameter_list.has_key(tuple[2]):
                newtuple[2] = '['+self.formal_parameter_list[tuple[2]]['address']+']'
            elif self.local_variable_list.has_key(tuple[2]):
                newtuple[2] = '['+self.local_variable_list[tuple[2]]+']'
                
            if self.is_integer(tuple[3]) or '$' in tuple[3]:
                newtuple[3] = tuple[3]
            elif self.formal_parameter_list.has_key(tuple[3]):
                newtuple[3] = '['+self.formal_parameter_list[tuple[3]]['address']+']'
            elif self.local_variable_list.has_key(tuple[2]):
                newtuple[3] = '['+self.local_variable_list[tuple[3]]+']'
            
            print newtuple   
            self.handle_IMULT(newtuple)
        elif tuple[1] == "IGE":
            newtuple = [tuple[0],tuple[1],'['+self.formal_parameter_list[tuple[2]]['address']+']',tuple[3]]
            self.handle_IGE(newtuple)
        elif tuple[1] == "ILT":            
            if self.formal_parameter_list.has_key(tuple[2]):
                newtuple = [tuple[0],tuple[1],'['+self.formal_parameter_list[tuple[2]]['address']+']',tuple[3]]
            elif self.local_variable_list.has_key(tuple[2]):
                newtuple = [tuple[0],tuple[1],'['+self.local_variable_list[tuple[2]]+']',tuple[3]]
            else:
                newtuple = [tuple[0],tuple[1],'['+tuple[2]+']',tuple[3]]           
            self.handle_ILT(newtuple)
        elif tuple[1] == "CJUMP":
            self.handle_CJUMP(tuple)
        elif tuple[1] == "JUMP":    
                self.handle_JUMP(tuple)
        elif tuple[1] == "LABEL":
            self.handle_LABEL(tuple)
        elif tuple[1] == "CALL":
            self.handle_CALL(tuple)
        elif tuple[1] == "MEMORY":
            self.handle_MEMORY(tuple)
        elif tuple[1] == "OUTPUTPARAMETER":
            newtuple = [tuple[0],tuple[1],tuple[2],tuple[3]]
            if self.local_variable_list.has_key(tuple[2]):                
                newtuple[2] = self.local_variable_list[tuple[2]]                
            elif self.formal_parameter_list.has_key(tuple[2]):
                temp = self.formal_parameter_list[tuple[2]]
                newtuple[2] = temp['address']
                if self.formal_parameter_list[tuple[2]]['type'] == 'REF':
                    register = self.get_register_holding_variable(temp['address'])
                    newtuple[2] = register['name']                                
            self.handle_OUTPUTPARAMETER(newtuple)
        elif tuple[1] == "OUTPUTSUBPARAMETER":
            self.handle_OUTPUTSUBPARAMETER(tuple)
        elif tuple[1] == "ENDOUTPUTPARAMETERS":
            self.handle_ENDOUTPUTPARAMETERS(tuple)
        elif tuple[1] == "END PROCEDURE":
            self.write_to_file('mov esp, ebp', 1)
            self.write_to_file('pop ebp', 1)
            self.write_to_file('ret', 0)
            self.in_procedure = ""        
        elif tuple[1] == 'BEGINACTUALPARAMETERLIST':
            del self.parameter_list[:]
        elif tuple[1] == 'ACTUALVPARAMETER':
            if not self.procedure_stack[-1]:
                self.parameter_list.append('['+tuple[2]+']')
            else:
                self.parameter_list.append('['+self.formal_parameter_list[tuple[2]]['address']+']')
        elif tuple[1] == 'ACTUALRPARAMETER':
            self.parameter_list.append(tuple[2])
        elif tuple[1] == 'ENDACTUALPARAMETERLIST':
            no_of_parameters = len(self.parameter_list)            
            while self.parameter_list:
                self.write_to_file("push dword "+self.parameter_list.pop(), 1)
            self.write_to_file("call "+self.in_procedure, 1)
            self.in_procedure = self.procedure_stack.pop()
            self.write_to_file('add esp, '+str(no_of_parameters*4), 1)
        elif tuple[1] == 'NOACTUALPARAMETERS':
            self.write_to_file("call "+self.in_procedure, 1)
            self.in_procedure = self.procedure_stack.pop()
                
    def add_declaration_section(self):
        self.write_to_file("popa \nmov     eax, 0 \nleave\nret\n\n\n\n"+self.bss_section_string+"\n\n\n"+self.data_section_string, 0) 
