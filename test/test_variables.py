# Copyright 2004-2010 Grant T. Olson.
# See license.txt for terms.

"""
Test various variables, parameters and constants in procedures
"""

from pyasm.x86asm import assembler, CDECL
from pyasm.x86cpToCoff import CpToCoff
import unittest
import os,sys
from linkCmd import linkCmd

class test_variables(unittest.TestCase):
    def test_params(self):
        """
        Make sure params get refrennced correctly
        """
        a = assembler()

        a.ADStr('hello_planets','3h + 12h + 12h = %xh\n\0')

        a.AP("_main")
        a.AI("PUSH EBX")
        a.AI("MOV EBX,0x12")
        a.AI("PUSH EBX")
        a.AI("MOV EBX,0x3")
        a.AI("PUSH EBX")
        a.AI("CALL get_x_plus_two_y")
        a.AI("PUSH EAX")
        a.AI("PUSH hello_planets")
        a.AI("CALL _printf")
        a.AI("ADD ESP,0x8") #printf is _cdecl
        #a.AI("XOR EAX,EAX")
        a.AI("POP EBX")
        a.EP()

        #get_planets proc
        a.AP("get_x_plus_two_y")
        a.AA("x")
        a.AA("y")
        a.AI("XOR EAX,EAX")
        a.AI("MOV EAX,x")
        a.AI("ADD EAX,y")
        a.AI("ADD EAX,y")
        a.EP()

        cp = a.Compile()
        
        coff = CpToCoff(cp,"-defaultlib:LIBCMT -defaultlib:OLDNAMES ").makeReleaseCoff()
        f = file("output/testParams.obj","wb")
        coff.WriteToFile(f)
        f.close()

        if sys.platform == 'win32':
            self.assertEquals(os.system(linkCmd("testParams")), 0)
            self.assertEquals(os.popen("cd output && testParams.exe").read(),
                              "3h + 12h + 12h = 27h\n")
        else:
            print "Skipping linker test, coff files are only valid on win32 platforms"
            
    def test_locals(self):
        """
        Make sure params get refrennced correctly
        """
        a = assembler()

        a.ADStr('hello_planets','3h + 12h + 12h = %xh\n\0')

        a.AP("_main")
        a.AI("CALL _get_x_plus_two_y")
        a.AI("PUSH EAX")
        a.AI("PUSH hello_planets")
        a.AI("CALL _printf")
        a.AI("XOR EAX,EAX")
        a.AI("ADD ESP,0x8") #printf is _cdecl
        a.EP()

        #get_planets proc
        a.AP("_get_x_plus_two_y")
        a.AddLocal("x")
        a.AddLocal("y")
        a.AI("MOV x,0x3")
        a.AI("MOV y,0x12")
        a.AI("XOR EAX,EAX")
        a.AI("MOV EAX,x")
        a.AI("ADD EAX,y")
        a.AI("ADD EAX,y")
        a.EP()

        cp = a.Compile()
        
        coff = CpToCoff(cp,"-defaultlib:LIBCMT -defaultlib:OLDNAMES ").makeReleaseCoff()
        f = file("output/testLocals.obj","wb")
        coff.WriteToFile(f)
        f.close()

        if sys.platform == 'win32':
            self.assertEquals(os.system(linkCmd("testLocals")), 0)
            self.assertEquals(os.popen("cd output && testlocals.exe").read(),
                              "3h + 12h + 12h = 27h\n")
        else:
            print "Skipping linker test, coff files are only valid on win32 platforms"

        
if __name__ == '__main__':
    unittest.main()
    
