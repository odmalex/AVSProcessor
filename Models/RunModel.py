
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
        self.videoTwoPass = task.getOptions()['videoTwoPass']
        avsFiles = task.getOptions()['avsFiles']
        totalFiles = task.getOptions()['filesNumber']

        if task.getOptions()['leonardoUse']:
            prefix = self.inputDirectory.split( '\\' )[-1]
            id = int( prefix )
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
            publisher.sendMessage( "QUEUE_PROCESSING_DIRECTORY",
                             task.getOptions()['outputDirectory'] )
            publisher.sendMessage( "QUEUE_PROCESSING_STATUS", 'In Progress' )
            task.setStatus( 'In Progress' )
        elif phase == 'finish':
            publisher.sendMessage( "QUEUE_PROCESSING_STATUS", 'Completed' )
            task.setStatus( 'Completed' )
        elif phase == 'finish_all':
            publisher.sendMessage( "PROCESSING_FINISH", '' )
            publisher.sendMessage( 'LOG', 'i9' )

    def avsFileLogging( self, phase, *args ):
        if phase == 'processing':
            publisher.sendMessage( "PROCESSING_FILE", 'Processing file: %s' %
                                   args[0] )
            publisher.sendMessage( "QUEUE_PROCESSED_FILES", '%d/%d' %
                                                      ( args[1], args[2] ) )
        elif phase == 'finished':
            publisher.sendMessage( "QUEUE_PROCESSED_FILES", '%d/%d' %
                                                      ( args[0], args[1] ) )

    def commandLogging( self, phase, *args ):
        if phase == 'init':
            publisher.sendMessage( "VIDEO_GAUGE", 0 )
            publisher.sendMessage( "VIDEO_LABEL", 'Extracting video...' )
            publisher.sendMessage( "AUDIO_GAUGE", 0 )
            publisher.sendMessage( "AUDIO_LABEL", 'Extracting audio...' )
            publisher.sendMessage( "MUX_GAUGE", 0 )
            publisher.sendMessage( "MUX_LABEL", 'Waiting for multiplexing...' )
        elif phase == 'video_start':
            publisher.sendMessage( "VIDEO_GAUGE", 0 )
            publisher.sendMessage( "VIDEO_LABEL", 'Extracting video... 0%' +
                                   args[0] )
        elif phase == 'video_during':
            publisher.sendMessage( 'LOG_VIDEO', args[0].strip( '\n' ) )
            publisher.sendMessage( "VIDEO_OUTPUT", args[0] )
            publisher.sendMessage( "VIDEO_GAUGE", args[1] )
            publisher.sendMessage( "VIDEO_LABEL", 'Extracting video... %d%%' %
                                   args[1] + args[2] )
        elif phase == 'video_finish':
            publisher.sendMessage( "VIDEO_GAUGE", 100 )
            publisher.sendMessage( "VIDEO_LABEL", 'Extracting video... 100%' +
                                   args[0] )
        elif phase == 'audio_start':
            publisher.sendMessage( "AUDIO_GAUGE", 0 )
            publisher.sendMessage( "AUDIO_LABEL", 'Extracting audio... 0%' )
        elif phase == 'audio_during':
            publisher.sendMessage( 'LOG_AUDIO', args[0].strip( '\n' ) )
            publisher.sendMessage( "AUDIO_OUTPUT", args[0] )
            publisher.sendMessage( "AUDIO_GAUGE", args[1] )
            publisher.sendMessage( "AUDIO_LABEL", 'Extracting audio... %d%%' %
                             args[1] )
        elif phase == 'audio_finish':
            publisher.sendMessage( "AUDIO_GAUGE", 100 )
            publisher.sendMessage( "AUDIO_LABEL", 'Extracting audio... 100%' )
        elif phase == 'mux_start':
            publisher.sendMessage( "MUX_GAUGE", 0 )
            publisher.sendMessage( "MUX_LABEL", 'Multiplexing... 0%' )
        elif phase == 'mux_during':
            publisher.sendMessage( 'LOG_MUX', args[0].strip( '\n' ) )
            publisher.sendMessage( "MUX_OUTPUT", args[0] )
            publisher.sendMessage( "MUX_GAUGE", args[1] )
            publisher.sendMessage( "MUX_LABEL", 'Multiplexing... %d%%' %
                             args[1] )
        elif phase == 'mux_finish':
            publisher.sendMessage( "MUX_GAUGE", 100 )
            publisher.sendMessage( "MUX_LABEL", 'Multiplexing... 100%' )

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
