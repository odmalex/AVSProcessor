import logging

class Logger:

    def __init__( self, name, filename, format, level = logging.DEBUG ):
        self.__log = None
        self.__fileHandler = None
        self.__streamHandler = None
        self.__formatter = None

        self.setLogger( name )
        self.setFileHandler( filename )
        self.setStreamHandler()
        self.setFormatter( format )
        self.setLevel( level )

    def setLogger( self, name ):
        self.__log = logging.getLogger( name )

    def setFileHandler( self, fileName ):
        self.__fileHandler = logging.FileHandler( fileName )
        self.__log.addHandler( self.__fileHandler )

    def setStreamHandler( self ):
        self.__streamHandler = logging.StreamHandler()
        self.__streamHandler.setLevel( logging.ERROR )
        self.__log.addHandler( self.__streamHandler )

    def setFormatter( self, format ):
        self.__formatter = logging.Formatter( format )
        self.__fileHandler.setFormatter( self.__formatter )
        self.__streamHandler.setFormatter( self.__formatter )

    def setLevel( self, level ):
        self.__log.setLevel( level )
        self.__fileHandler.setLevel( level )

    def trace( self, type, message ):
        if type == 'INFO':
            self.__log.info( message )
        elif type == 'ERROR':
            self.__log.error( message )
        elif type == 'CRITICAL':
            self.__log.critical( message )


if __name__ == '__main__':
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    l = Logger( 'temp', '.\\temp', format )
    l.trace( 'INFO', 'Hello' )
