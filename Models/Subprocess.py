
from subprocess import Popen, PIPE, STDOUT
from pprint import pprint

class Subprocess:
    def __init__( self, command ):
        self._command = command

    def execute( self ):
        self.process = Popen( self._command, universal_newlines = True, stdout = PIPE,
              stderr = STDOUT, shell = True )

    def readline( self ):
        return self.process.stdout.readline()

    def poll( self ):
        return self.process.poll()
