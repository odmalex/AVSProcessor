
from Commands import Commands
from Configuration import Configuration
from pubsub import  pub
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
from pprint import pprint
from Subprocess import Subprocess
publisher = pub.Publisher()

class LeonardoSettingsModel:
    def __init__( self ):
        self.leonardo = Configuration.get( 'leonardo' )

    def loadLists( self ):
        languages = sorted( self.leonardo['language_list'].keys() )
        variants = sorted( self.leonardo['variant_list'].keys() )
        owners = sorted( self.leonardo['owner_list'].keys() )
        aspectRatios = sorted( self.leonardo['aspect_ratio_list'].keys() )
        copyrights = sorted( self.leonardo['copyright_list'].keys() )

        return [languages, variants, owners, aspectRatios, copyrights]



