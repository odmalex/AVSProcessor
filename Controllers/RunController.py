import wx
import os
from Views.RunView import RunView
from Models.RunModel import RunModel
from Models.QC import QC
from Models.Configuration import Configuration
from pubsub import  pub
from threading import Thread
publisher = pub.Publisher()

class RunController:
    def __init__( self, taskQueue ):

        self.taskQueue = taskQueue

        self.runView = RunView( None, -1, "" )
        self.runView.Show()
        self.setSubscriber()

        self.runModel = RunModel( self.taskQueue )
#        self.runAll()
        Thread( target = self.runAll ).start()


    def exiting( self, message ):
        self.runView.Destroy()

    def setSubscriber( self ):
        pub.subscribe( self.updateProcessingFile, 'PROCESSING_FILE' )
        pub.subscribe( self.updateVideoGauge, 'VIDEO_GAUGE' )
        pub.subscribe( self.updateVideoLabel, 'VIDEO_LABEL' )
        pub.subscribe( self.updateVideoOutput, 'VIDEO_OUTPUT' )
        pub.subscribe( self.updateAudioGauge, 'AUDIO_GAUGE' )
        pub.subscribe( self.updateAudioLabel, 'AUDIO_LABEL' )
        pub.subscribe( self.updateAudioOutput, 'AUDIO_OUTPUT' )
        pub.subscribe( self.updateMuxGauge, 'MUX_GAUGE' )
        pub.subscribe( self.updateMuxLabel, 'MUX_LABEL' )
        pub.subscribe( self.updateMuxOutput, 'MUX_OUTPUT' )
        pub.subscribe( self.processingFinish, 'PROCESSING_FINISH' )
        pub.subscribe( self.exiting, 'EXITING' )

    def runAll( self ):
        pub.sendMessage( 'QUEUE_PROCESSING_STATUSES', arg1='Pending' )
        for task in self.taskQueue:
            if not task.getStatus() == 'Completed':
                task.setStatus( 'Pending' )
        self.runModel.processAll()

    def processingFinish( self, message ):
        self.runView.Destroy()


    def updateProcessingFile( self, arg1 ):
        self.runView.setProcessingFileText( arg1 )

    def updateVideoGauge( self, arg1 ):
        self.runView.videoExtractGauge.SetValue( arg1 )

    def updateVideoLabel( self, arg1 ):
        self.runView.videoExtractStaticText.SetLabel( arg1 )

    def updateVideoOutput( self, arg1 ):
        self.runView.videoDetailsTextCtrl.AppendText( arg1 )
        self.runView.videoDetailsTextCtrl.SetStyle( -1, -1, wx.TextAttr( "white" ) )

    def updateAudioGauge( self, arg1 ):
        self.runView.audioExtractGauge.SetValue( arg1 )

    def updateAudioLabel( self, arg1 ):
        self.runView.audioExtractStaticText.SetLabel( arg1 )

    def updateAudioOutput( self, arg1 ):
        self.runView.audioDetailsTextCtrl.AppendText( arg1 )
        self.runView.audioDetailsTextCtrl.SetStyle( -1, -1, wx.TextAttr( "white" ) )

    def updateMuxGauge( self, arg1 ):
        self.runView.muxGauge.SetValue( arg1 )

    def updateMuxLabel( self, arg1 ):
        self.runView.muxStaticText.SetLabel( arg1 )

    def updateMuxOutput( self, arg1 ):
        self.runView.muxDetailsTextCtrl.AppendText( arg1 )
        self.runView.muxDetailsTextCtrl.SetStyle( -1, -1, wx.TextAttr( "white" ) )

