import argparse
import sys
sys.path.append( 'C:\\Python27\\Lib\\site-packages\\wx-2.8-msw-unicode' )
from Models.Configuration import Configuration
from Models.QC import QC
from Models.Commands import Commands
from Models.RunModel import RunModel

parser = argparse.ArgumentParser( description = 'Short sample app' )

parser.add_argument( '-i', action = "store", dest = "inputDirectory", help = "The input directory" )
parser.add_argument( '-o', action = "store", dest = "outputDirectory", help = "The output directory" )
parser.add_argument( '-p', action = "store", dest = "profile", help = "The name of the chosen profile" )
parser.add_argument( '-l', action = "store", dest = "leonardo_settings", help = "Example: NLD:FEA:ODM:CPY:169" )
parser.add_argument( '-f', action = "store", dest = "conf_file", default = "conf\\avs.ini", help = "The configuration file" )
parser.add_argument( '--lp', action = "store_true", default = 'False', help = "Lists all the available profiles" )
parser.add_argument( '--twopass', action = "store_true", default = 'False', help = "The video will be extracted twice" )
parser.add_argument( '--fs', action = "store_true", default = 'False', help = "Frequency sample 44100 will be used" )


class Avsprocessor:
    def __init__( self ):
        self.args = parser.parse_args()
        self.checkConfFile()

        if len( sys.argv ) == 2 and self.args.lp:
            self.listProfiles()
        else:
            print self.args


    def listProfiles( self ):
        profiles = QC.loadFiles( Configuration.all['directories']['profile'], 'prfl' )
        for profile in profiles:
            print profile

    def checkConfFile( self ):
        Configuration.load( self.args.conf_file )




if __name__ == '__main__':

    Avsprocessor()


