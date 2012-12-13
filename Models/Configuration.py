
import json

class Configuration:
    configurationFile = '..\\conf\\avs.ini'
    databaseFile = '..\\conf\\db.ini'
    all = {}
    db_conn = {}

    ##################### Load & Save configuration
    @staticmethod
    def load( inputFile ):
        try:
            with open( inputFile ) as f:
                content = f.read()
            return json.JSONDecoder().decode( content )
        except:
            print 'Error in loading file: "' + inputFile + '". Exiting...'
            #self.logger_core.critical( "Error in loading configuration. Exiting..." )
            exit()

    @staticmethod
    def save( outputFile ):
        try:
            s = json.dumps( Configuration.all, sort_keys = True, indent = 4 )
            f = open( outputFile, 'w' )
            f.write( s + "\n" )
            f.close()
        except:
            #self.logger_core.critical( "Error while saving configuration. Configuration was not saved." )
            pass

    @staticmethod
    def set( value, *kwds ):
        if len( kwds ) == 1:
            Configuration.all[ kwds[0] ] = value
        elif len( kwds ) == 2:
            Configuration.all[ kwds[0] ][ kwds[1] ] = value
        elif len( kwds ) == 3:
            Configuration.all[ kwds[0] ][ kwds[1] ][ kwds[2] ] = value

    @staticmethod
    def get( *kwds ):
        if len( kwds ) == 1:
            return Configuration.all[ kwds[0] ]
        elif len( kwds ) == 2:
            return Configuration.all[ kwds[0] ][ kwds[1] ]
        elif len( kwds ) == 3:
            return Configuration.all[ kwds[0] ][ kwds[1] ][ kwds[2] ]

if __name__ == '__main__':
    Configuration.load( 'avs_processor.conf' )
    print Configuration.get( 'directories', 'host' )
    Configuration.set( 'C:\\OD_Encoding', 'directories', 'host' )
    Configuration.save( 'avs_processor.conf' )
    Configuration.load( 'avs_processor.conf' )
    print Configuration.get( 'directories', 'host' )
