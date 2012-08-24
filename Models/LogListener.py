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

        publisher.subscribe( self.logCore, 'LOG' )
        publisher.subscribe( self.logVideo, 'LOG_VIDEO' )
        publisher.subscribe( self.logAudio, 'LOG_AUDIO' )
        publisher.subscribe( self.logMux, 'LOG_MUX' )

    def logCore( self, message ):
        msg = self.log_map[message.data]
        if message.data[0] == 'i':
            type = 'INFO'
        elif message.data[0] == 'e':
            type = 'ERROR'
        elif message.data[0] == 'c':
            type = 'CRITICAL'
        self.coreLogger.trace( type, msg )

    def logVideo( self, message ):
        self.videoLogger.trace( 'INFO', message.data )

    def logAudio( self, message ):
        self.audioLogger.trace( 'INFO', message.data )

    def logMux( self, message ):
        self.muxLogger.trace( 'INFO', message.data )


