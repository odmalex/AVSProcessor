
from Models.DB import DB
from Commands import Commands
from Configuration import Configuration
from pubsub import  pub
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
from pprint import pprint
from Subprocess import Subprocess
import datetime
publisher = pub.Publisher()

class RunModel:
    def __init__( self, taskQueue ):
        self.taskQueue = taskQueue
        self.db = DB()

    def setCommands( self, commands ):
        self.__commands = commands
        self.__vcommand = self.__commands[0]
        self.__acommand = self.__commands[1]
        self.__mcommand = self.__commands[2]


    def processAll( self ):
        for task in self.taskQueue:
            if task.getStatus() == 'Completed':
                continue
            t = Thread( target = self.processTask, args = ( task, ) )

            t.start()
            self.taskLogging( 'start', task )

            t.join()
            self.taskLogging( 'finish', task )

        self.taskLogging( 'finish_all' )

    def processTask( self, task ):
        self.inputDirectory = task.getOptions()['inputDirectory']
        self.videoTwoPass   = task.getOptions()['videoTwoPass']
        avsFiles            = task.getOptions()['avsFiles']
        totalFiles          = task.getOptions()['filesNumber']

        if task.getOptions()['leonardoUse']:
            prefix = self.inputDirectory.split( '\\' )[-1]
            id     = int( prefix )
            self.db.updateTable( 'title', id, 'start_timestamp', datetime.datetime.now() )

        i = 0
        for avs in avsFiles:
            self.com = Commands( task )
            commands = self.com.getCommands( avs )
            self.setCommands( commands )

            self.avsFileLogging( 'processing', avs, i, totalFiles )
            c = Thread( target = self.runCommands, args = () )
            c.start()
            c.join()
            i += 1
        self.avsFileLogging( 'finished', i, totalFiles )

        if task.getOptions()['leonardoUse']:
            self.db.updateTable( 'title', id, 'end_timestamp', datetime.datetime.now() )
            self.db.updateTable( 'title', id, 'status', 'Completed' )

    def runCommands( self ):
        self.commandLogging( 'init' )

        v = Thread( target = self.extractVideo, args = ( False, ) )
        a = Thread( target = self.extractAudio, args = () )
        m = Thread( target = self.mux, args = () )
        v.start()
        a.start()
        v.join()

        if self.videoTwoPass:
            v2 = Thread( target = self.extractVideo, args = ( True, ) )
            v2.start()
            v2.join()

        a.join()
        m.start()
        m.join()

    def extractVideo( self, twopass ):
        extra = ''
        if twopass:
            extra = ' -- second pass'
        else:
            extra = ''

        self.commandLogging( 'video_start', extra )
        video_process = Subprocess( self.__vcommand )
        video_process.execute()
        while ( video_process.poll() is None ):
            try:
                line = video_process.readline()
                perc = self.parseLine( 'video', line )
                if perc == -1:
                    break
                self.commandLogging( 'video_during', line, perc, extra )
            except:
                pass
        self.commandLogging( 'video_finish', extra )

    def extractAudio( self ):
        self.commandLogging( 'audio_start' )
        audio_process = Subprocess( self.__acommand )
        audio_process.execute()

        while ( audio_process.poll() is None ):
            try:
                line = audio_process.readline()
                perc = self.parseLine( 'audio', line )
                self.commandLogging( 'audio_during', line, perc )
            except:
                pass
        self.commandLogging( 'audio_finish' )

    def mux( self ):
        self.commandLogging( 'mux_start' )
        mux_process = Subprocess( self.__mcommand )
        mux_process.execute()
        while ( mux_process.poll() is None ):
            try:
                line = mux_process.readline()
                perc = self.parseLine( 'mux', line )
                self.commandLogging( 'mux_during', line, perc )
            except:
                pass
        self.commandLogging( 'mux_finish' )

    def taskLogging( self, phase, task = None ):
        if phase == 'start':
            pub.sendMessage( "QUEUE_PROCESSING_DIRECTORY",
                             arg1=task.getOptions()['outputDirectory'] )
            pub.sendMessage( "QUEUE_PROCESSING_STATUS", arg1='In Progress' )
            task.setStatus( 'In Progress' )
        elif phase == 'finish':
            pub.sendMessage( "QUEUE_PROCESSING_STATUS", arg1='Completed' )
            task.setStatus( 'Completed' )
        elif phase == 'finish_all':
            pub.sendMessage( "PROCESSING_FINISH", message='' )
            pub.sendMessage( 'LOG', arg1='i9' )

    def avsFileLogging( self, phase, *args ):
        if phase == 'processing':
            pub.sendMessage( "PROCESSING_FILE", arg1='Processing file: %s' %
                                   args[0] )
            sendData = '%d/%d' % ( args[1], args[2] )
           
            pub.sendMessage( "QUEUE_PROCESSED_FILES", arg1=sendData )
        elif phase == 'finished':
            pub.sendMessage( "QUEUE_PROCESSED_FILES", arg1=('%d/%d' %
                                                      ( args[0], args[1] )) )

    def commandLogging( self, phase, *args ):
        if phase == 'init':
            pub.sendMessage( "VIDEO_GAUGE", arg1=0 )
            pub.sendMessage( "VIDEO_LABEL", arg1='Extracting video...' )
            pub.sendMessage( "AUDIO_GAUGE", arg1=0 )
            pub.sendMessage( "AUDIO_LABEL", arg1='Extracting audio...' )
            pub.sendMessage( "MUX_GAUGE", arg1=0 )
            pub.sendMessage( "MUX_LABEL", arg1='Waiting for multiplexing...' )
        elif phase == 'video_start':
            pub.sendMessage( "VIDEO_GAUGE", arg1=0 )
            pub.sendMessage( "VIDEO_LABEL", arg1='Extracting video... 0%' +
                                   args[0] )
        elif phase == 'video_during':
            pub.sendMessage( 'LOG_VIDEO', arg1=args[0].strip( '\n' ) )
            pub.sendMessage( "VIDEO_OUTPUT", arg1=args[0] )
            pub.sendMessage( "VIDEO_GAUGE", arg1=args[1] )
            pub.sendMessage( "VIDEO_LABEL", arg1='Extracting video... %d%%' %
                                   args[1] + args[2] )
        elif phase == 'video_finish':
            pub.sendMessage( "VIDEO_GAUGE", arg1=100 )
            pub.sendMessage( "VIDEO_LABEL", arg1='Extracting video... 100%' +
                                   args[0] )
        elif phase == 'audio_start':
            pub.sendMessage( "AUDIO_GAUGE", arg1=0 )
            pub.sendMessage( "AUDIO_LABEL", arg1='Extracting audio... 0%' )
        elif phase == 'audio_during':
            pub.sendMessage( 'LOG_AUDIO', arg1=args[0].strip( '\n' ) )
            pub.sendMessage( "AUDIO_OUTPUT", arg1=args[0] )
            pub.sendMessage( "AUDIO_GAUGE", arg1=args[1] )
            pub.sendMessage( "AUDIO_LABEL", arg1='Extracting audio... %d%%' %
                             args[1] )
        elif phase == 'audio_finish':
            pub.sendMessage( "AUDIO_GAUGE", arg1=100 )
            pub.sendMessage( "AUDIO_LABEL", arg1='Extracting audio... 100%' )
        elif phase == 'mux_start':
            pub.sendMessage( "MUX_GAUGE", arg1=0 )
            pub.sendMessage( "MUX_LABEL", arg1='Multiplexing... 0%' )
        elif phase == 'mux_during':
            pub.sendMessage( 'LOG_MUX', arg1=args[0].strip( '\n' ) )
            pub.sendMessage( "MUX_OUTPUT", arg1=args[0] )
            pub.sendMessage( "MUX_GAUGE", arg1=args[1] )
            pub.sendMessage( "MUX_LABEL", arg1='Multiplexing... %d%%' %
                             args[1] )
        elif phase == 'mux_finish':
            pub.sendMessage( "MUX_GAUGE", arg1=100 )
            pub.sendMessage( "MUX_LABEL", arg1='Multiplexing... 100%' )

    def parseLine( self, type, line ):
        if type == 'video':
            try:
                if line.split()[0] == 'encoded':
                    return -1
                perc = line.split( '[' )[1].split( '.' )[0]
                return int( perc )
            except:
                pass
        elif type == 'audio':
            try:
                perc = line.split( '[' )[1].split( '.' )[0]
    #            perc = line.split( '%' )[0].split( '>>>' )[1].split( '.' )[0]
                return int( perc.strip() )
            except:
                pass
        elif type == 'mux':
            try:
                perc = int( line.split( '(' )[1].split( '/' )[0] )
                tokens = line.split()
                if tokens[1] == 'ISO':
                    perc += 100
                elif tokens[1] == 'File':
                    perc += 200
                return int( int( perc ) / 3 )
            except:
                pass

if __name__ == '__main__':
    pass
