
from Models.QC import QC
from Models.Configuration import Configuration

class Task:

    def __init__( self ):

        self.__options = {}

    def loadOptions( self, id, opt ):

        self.__options['id'] = id
        self.__options['inputDirectory'] = opt['inputDirectory']
        self.__options['outputDirectory'] = opt['outputDirectory']
        self.__options['profileDirectory'] = opt['profileDirectory']
        self.__options['profile'] = opt['profile']
        self.__options['videoOutputFormat'] = opt['videoOutputFormat']
        self.__options['videoCmdOptions'] = opt['videoCmdOptions']
        self.__options['videoTwoPass'] = opt['videoTwoPass']
        self.__options['audioOutputFormat'] = opt['audioOutputFormat']
        self.__options['audioCmdOptions'] = opt['audioCmdOptions']
        self.__options['audioBitrate'] = opt['audioBitrate']
        self.__options['audioFrequencySample'] = opt['audioFrequencySample']
        self.__options['muxOutputFormat'] = opt['muxOutputFormat']
        self.__options['leonardoUse'] = opt['leonardoUse']

        self.__options['avsFiles'] = QC.loadFiles( self.__options['inputDirectory'],
                                                 'avs' )
        self.__options['filesNumber'] = len( self.__options['avsFiles'] )
        self.__options['status'] = ''

    def setStatus( self, s ):
        self.__options['status'] = s

    def getStatus( self ):
        return self.__options['status']

    def getOptions( self ):
        return self.__options
