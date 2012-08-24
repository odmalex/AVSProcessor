
from Commands import Commands
from Configuration import Configuration
from pubsub import  pub
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
from pprint import pprint
publisher = pub.Publisher()

class RunModel:
    def __init__( self, taskQueue ):
        self.taskQueue = taskQueue

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
            publisher.sendMessage( "QUEUE_PROCESSING_DIRECTORY",
                             task.getOptions()['outputDirectory'] )
            publisher.sendMessage( "QUEUE_PROCESSING_STATUS", 'In Progress' )
            task.setStatus( 'In Progress' )
            t.join()
            publisher.sendMessage( "QUEUE_PROCESSING_STATUS", 'Completed' )
            task.setStatus( 'Completed' )
        publisher.sendMessage( "PROCESSING_FINISH", '' )
        publisher.sendMessage( 'LOG', 'i9' )

    def processTask( self, task ):
        self.inputDirectory = task.getOptions()['inputDirectory']
        self.videoTwoPass = task.getOptions()['videoTwoPass']
        avsFiles = task.getOptions()['avsFiles']
        totalFiles = task.getOptions()['filesNumber']

        i = 0
        for avs in avsFiles:
            self.com = Commands( task )
            commands = self.com.getCommands( avs )
            self.setCommands( commands )

            publisher.sendMessage( "PROCESSING_FILE", 'Processing file: %s' % avs )
            publisher.sendMessage( "QUEUE_PROCESSED_FILES", '%d/%d' %
                                                      ( i, totalFiles ) )
            c = Thread( target = self.runCommands, args = () )
            c.start()
            c.join()
            i += 1
        publisher.sendMessage( "QUEUE_PROCESSED_FILES", '%d/%d' %
                                                      ( i, totalFiles ) )

    def runCommands( self ):
        publisher.sendMessage( "VIDEO_GAUGE", 0 )
        publisher.sendMessage( "VIDEO_LABEL", 'Extracting video...' )
        publisher.sendMessage( "AUDIO_GAUGE", 0 )
        publisher.sendMessage( "AUDIO_LABEL", 'Extracting audio...' )
        publisher.sendMessage( "MUX_GAUGE", 0 )
        publisher.sendMessage( "MUX_LABEL", 'Waiting for multiplexing...' )

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

        publisher.sendMessage( "VIDEO_GAUGE", 0 )
        publisher.sendMessage( "VIDEO_LABEL", 'Extracting video... 0%' + extra )
        proc = Popen( self.__vcommand, universal_newlines = True, stdout = PIPE,
                      stderr = STDOUT, shell = True )
        while ( proc.poll() is None ):
            try:
                line = proc.stdout.readline()
                publisher.sendMessage( 'LOG_VIDEO', line.strip( '\n' ) )
                publisher.sendMessage( "VIDEO_OUTPUT", line )
                if line.split()[0] == 'encoded':
                    break
                perc = line.split( '[' )[1].split( '.' )[0]
                self.videoCurr = int( perc )
                publisher.sendMessage( "VIDEO_GAUGE", self.videoCurr )
                publisher.sendMessage( "VIDEO_LABEL", 'Extracting video... %d%%' %
                                 self.videoCurr + extra )
            except:
                pass

        publisher.sendMessage( "VIDEO_GAUGE", 100 )
        publisher.sendMessage( "VIDEO_LABEL", 'Extracting video... 100%' + extra )

    def extractAudio( self ):
        publisher.sendMessage( "AUDIO_GAUGE", 0 )
        publisher.sendMessage( "AUDIO_LABEL", 'Extracting audio... 0%' )
        proc = Popen( self.__acommand, universal_newlines = True, stdout = PIPE,
                      stderr = STDOUT, shell = True )
        while ( proc.poll() is None ):
            try:
                line = proc.stdout.readline()
                publisher.sendMessage( 'LOG_AUDIO', line.strip( '\n' ) )
                publisher.sendMessage( "AUDIO_OUTPUT", line )
                perc = line.split( '[' )[1].split( '.' )[0]
#                perc = line.split( '%' )[0].split( '>>>' )[1].split( '.' )[0]
                self.audioCurr = int( perc.strip() )
                publisher.sendMessage( "AUDIO_GAUGE", self.audioCurr )
                publisher.sendMessage( "AUDIO_LABEL", 'Extracting audio... %d%%' %
                                 self.audioCurr )
            except:
                pass

        publisher.sendMessage( "AUDIO_GAUGE", 100 )
        publisher.sendMessage( "AUDIO_LABEL", 'Extracting audio... 100%' )

    def mux( self ):
        proc = Popen( self.__mcommand, universal_newlines = True, stdout = PIPE,
                      stderr = STDOUT, shell = True )

        while ( proc.poll() is None ):
            try:
                line = proc.stdout.readline()
                publisher.sendMessage( 'LOG_MUX', line.strip( '\n' ) )
                publisher.sendMessage( "MUX_OUTPUT", line )
                perc = int( line.split( '(' )[1].split( '/' )[0] )
                tokens = line.split()
                if tokens[1] == 'ISO':
                    perc += 100
                elif tokens[1] == 'File':
                    perc += 200
                self.muxCurr = int( int( perc ) / 3 )
                publisher.sendMessage( "MUX_GAUGE", self.muxCurr )
                publisher.sendMessage( "MUX_LABEL", 'Multiplexing... %d%%' %
                                 self.muxCurr )
            except:
                pass

        publisher.sendMessage( "MUX_GAUGE", 100 )
        publisher.sendMessage( "MUX_LABEL", 'Multiplexing... 100%' )


if __name__ == '__main__':
    pass
