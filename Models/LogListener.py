import os
from Logger import Logger
from pubsub import  pub
publisher = pub.Publisher()

class LogListener:
    def __init__( self, logDir ):

        self.log_map = {
               'i1': 'AVS Processor started',
               'i2': 'Loading configuration',
               'i3': 'Checking directories',
               'i4': 'Checking applications and libraries',
               'i5': 'New host directory was specified by the user',
               'i6': 'New task was added to the list',
               'i7': 'Task was removed from the list',
               'i8': 'Processing started for all the items of the list',
               'i9': 'Processing finished for all the items of the list',
               'i10': 'Exiting...',
               'e1': 'Error in checking host directory. Directory "." \
                       will be used instead',
               'e2': 'Error in checking log directory. Directory "." \
                       will be used instead',
               'c1': 'Error in loading configuration! Exiting...',
               'c2': 'Error in checking applications! Exiting...',
               'c3': 'Error in checking libraries! Exiting...',

               }

        self.logDir = logDir
        self.formatting = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

        self.coreLogger = Logger( 'core',
                                  os.path.join( self.logDir, 'core.log' ),
                                  self.formatting )
        self.videoLogger = Logger( 'video',
                                   os.path.join( self.logDir, 'video.log' ),
                                   self.formatting )
        self.audioLogger = Logger( 'audio',
                                   os.path.join( self.logDir, 'audio.log' ),
                                   self.formatting )
        self.muxLogger = Logger( 'mux',
                                 os.path.join( self.logDir, 'mux.log' ),
                                 self.formatting )

        pub.subscribe( self.logCore, 'LOG' )
        pub.subscribe( self.logVideo, 'LOG_VIDEO' )
        pub.subscribe( self.logAudio, 'LOG_AUDIO' )
        pub.subscribe( self.logMux, 'LOG_MUX' )

    def logCore( self, arg1 ):
        msg = self.log_map[arg1]
        if arg1[0] == 'i':
            type = 'INFO'
        elif arg1[0] == 'e':
            type = 'ERROR'
        elif arg1[0] == 'c':
            type = 'CRITICAL'
        self.coreLogger.trace( type, msg )

    def logVideo( self, arg1 ):
        self.videoLogger.trace( 'INFO', arg1 )

    def logAudio( self, arg1 ):
        self.audioLogger.trace( 'INFO', arg1 )

    def logMux( self, arg1 ):
        self.muxLogger.trace( 'INFO', arg1 )


