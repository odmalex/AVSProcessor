from Configuration import Configuration
import os
from pprint import pprint

class Commands:
    def __init__( self, task ):
        self.task = task
        self.input_avs = ''
        self.output_video = ''
        self.output_audio = ''
        self.output_mux = ''

    def getConf( self ):
        self.inputDirectory = self.task.getOptions()[ 'inputDirectory']
        self.outputDirectory = self.task.getOptions()[ 'outputDirectory']
        self.videoOutputFormat = self.task.getOptions()[ 'videoOutputFormat']
        self.videoCmdOptions = self.task.getOptions()[ 'videoCmdOptions']
        self.audioOutputFormat = self.task.getOptions()[ 'audioOutputFormat']
        self.audioBitrate = self.task.getOptions()[ 'audioBitrate']
        self.audioFrequencySample = self.task.getOptions()['audioFrequencySample']
        self.muxOutputFormat = self.task.getOptions()[ 'muxOutputFormat']
        self.hostDirectory = Configuration.all[ 'directories'][ 'host' ]
        self.applications = Configuration.all[ 'applications' ]

    def getCommands( self, inputFile ):
        self.getConf()
        filename, extension = os.path.splitext( inputFile )
        self.input_avs = os.path.join( self.inputDirectory, inputFile )

        self.output_video = os.path.join( self.outputDirectory,
                                     os.path.basename( filename ) ) + \
                                     '.' + self.videoOutputFormat

        self.output_audio = os.path.join( self.outputDirectory,
                                     os.path.basename( filename ) ) + \
                                     '.audio.' + self.audioOutputFormat

        self.output_mux = os.path.join( self.outputDirectory,
                                   os.path.basename( filename ) ) + \
                                   '.' + self.muxOutputFormat

        return [self.video(), self.audio(), self.mux()]


    def video( self ):
        x264 = os.path.join( self.hostDirectory,
                        os.path.basename( self.applications["x264"] ) )

        videoExtraction = ''
        videoExtraction += '"' + x264 + '" ' + self.videoCmdOptions + \
                           ' -o ' + '"' + self.output_video + '" ' + '"' + \
                           self.input_avs + '"'
        return videoExtraction

    def audio( self ):
#        avs2wav = os.path.join( self.hostDirectory,
#                        os.path.basename( self.applications["avs2wav"] ) )
#        neroaacenc = os.path.join( self.hostDirectory,
#                        os.path.basename( self.applications["neroaacenc"] ) )
        avs2pipe = os.path.join( self.hostDirectory,
                        os.path.basename( self.applications["avs2pipe"] ) )
        qaac = os.path.join( self.hostDirectory,
                        os.path.basename( self.applications["qaac"] ) )

        audioExtraction = ''
        audioExtraction += '"' + avs2pipe + '" -wav "' + self.input_avs + \
                           '" | "' + qaac + '" - -c ' + \
                           str( int( self.audioBitrate ) / 1000 )
        if self.audioFrequencySample:
            audioExtraction += ' --rate 44100'
        audioExtraction += ' -o "' + self.output_audio + '"'

#        audioExtraction += '"' + avs2wav + '" "' + Commands.input_avs + '" - | "' \
#                        + neroaacenc + '" -cbr -lc -br ' + \
#                        Commands.audioBitrate + \
#                        ' -if - -of "' + Commands.output_audio + '"'
        return audioExtraction


    def mux( self ):
        mp4box = os.path.join( self.hostDirectory,
                        os.path.basename( self.applications["mp4box"] ) )

        multiplexing = ''
        multiplexing += '"' + mp4box + '" -fps 25 -add "' + \
                        self.output_video + '" -add "' + \
                        self.output_audio + '" "' + \
                        self.output_mux + '"'
        return multiplexing

if __name__ == '__main__':
    Configuration.load( 'avs_processor.conf' )
    Configuration.set( 'C:\\Users\\Administrator\\Desktop\\in' , 'directories',
                        'input' )
    Configuration.set( 'C:\\Users\\Administrator\\Desktop\\out' , 'directories',
                        'output' )
    Configuration.set( 'C:\\OD_Encoding' , 'directories',
                        'host' )

    Configuration.set( 'x264', 'videoSettings', 'outputFormat' )
    Configuration.set( '--profile main --level 3.1 --preset slow --bitrate \
1500 --no-cabac --bframes 3 --ref 1 --b-pyramid 0 \
--keyint 50 --min-keyint 50 --no-scenecut \
--rc-lookahead 50', 'videoSettings', 'cmdOptions' )

    Configuration.set( 'MP4', 'audioSettings', 'outputFormat' )
    Configuration.set( '64000', 'audioSettings', 'bitrate' )
    Configuration.set( 'MP4', 'muxSettings', 'outputFormat' )

    pprint ( Commands.getCommands( 'DOR_80_256_ Linfirmiere_The_Nurse_VANG_169_HD_PAL.avs' ) )
