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
        Thread( target = self.runAll ).start()


    def exiting( self, message ):
        self.runView.Destroy()

    def setSubscriber( self ):
        publisher.subscribe( self.updateProcessingFile, 'PROCESSING_FILE' )
        publisher.subscribe( self.updateVideoGauge, 'VIDEO_GAUGE' )
        publisher.subscribe( self.updateVideoLabel, 'VIDEO_LABEL' )
        publisher.subscribe( self.updateVideoOutput, 'VIDEO_OUTPUT' )
        publisher.subscribe( self.updateAudioGauge, 'AUDIO_GAUGE' )
        publisher.subscribe( self.updateAudioLabel, 'AUDIO_LABEL' )
        publisher.subscribe( self.updateAudioOutput, 'AUDIO_OUTPUT' )
        publisher.subscribe( self.updateMuxGauge, 'MUX_GAUGE' )
        publisher.subscribe( self.updateMuxLabel, 'MUX_LABEL' )
        publisher.subscribe( self.updateMuxOutput, 'MUX_OUTPUT' )
        publisher.subscribe( self.processingFinish, 'PROCESSING_FINISH' )
        publisher.subscribe( self.exiting, 'EXITING' )

    def runAll( self ):
        publisher.sendMessage( 'QUEUE_PROCESSING_STATUSES', 'Pending' )
        for task in self.taskQueue:
            if not task.getStatus() == 'Completed':
                task.setStatus( 'Pending' )
        self.runModel.processAll()

    def processingFinish( self, message ):
        self.runView.Destroy()


    def updateProcessingFile( self, message ):
        self.runView.setProcessingFileText( message.data )

    def updateVideoGauge( self, message ):
        self.runView.videoExtractGauge.SetValue( message.data )

    def updateVideoLabel( self, message ):
        self.runView.videoExtractStaticText.SetLabel( message.data )

    def updateVideoOutput( self, message ):
        self.runView.videoDetailsTextCtrl.AppendText( message.data )
        self.runView.videoDetailsTextCtrl.SetStyle( -1, -1, wx.TextAttr( "white" ) )

    def updateAudioGauge( self, message ):
        self.runView.audioExtractGauge.SetValue( message.data )

    def updateAudioLabel( self, message ):
        self.runView.audioExtractStaticText.SetLabel( message.data )

    def updateAudioOutput( self, message ):
        self.runView.audioDetailsTextCtrl.AppendText( message.data )
        self.runView.audioDetailsTextCtrl.SetStyle( -1, -1, wx.TextAttr( "white" ) )

    def updateMuxGauge( self, message ):
        self.runView.muxGauge.SetValue( message.data )

    def updateMuxLabel( self, message ):
        self.runView.muxStaticText.SetLabel( message.data )

    def updateMuxOutput( self, message ):
        self.runView.muxDetailsTextCtrl.AppendText( message.data )
        self.runView.muxDetailsTextCtrl.SetStyle( -1, -1, wx.TextAttr( "white" ) )

