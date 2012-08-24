import wx
import os
from Views.x264View import x264View
from Models.x264Model import x264Model
from Models.Configuration import Configuration
from Models.QC import QC
from PreviewController import PreviewController
from RunController import RunController
from pubsub import  pub
publisher = pub.Publisher()

class x264Controller:
    def __init__( self, panel ):
        self.x264 = panel
        self.x264Model = x264Model()
        self.loadOptions()

        publisher.subscribe( self.updateQueueProcessingDirectory,
                       'QUEUE_PROCESSING_DIRECTORY' )
        publisher.subscribe( self.updateQueueProcessedFiles, 'QUEUE_PROCESSED_FILES' )
        publisher.subscribe( self.updateQueueProcessingStatus,
                       'QUEUE_PROCESSING_STATUS' )
        publisher.subscribe( self.updateQueueProcessingStatuses,
                       'QUEUE_PROCESSING_STATUSES' )
        publisher.subscribe( self.processingFinish, 'PROCESSING_FINISH' )

    def processingFinish( self, message ):
        self.x264.enableButtons()

    def updateQueueProcessingDirectory( self, message ):
        self.currentProcessingDirectory = message.data

    def updateQueueProcessedFiles( self, message ):
        self.updateColumns( 1, message.data )

    def updateQueueProcessingStatus( self, message ):
        self.updateColumns( 2, message.data )

    def updateQueueProcessingStatuses( self, message ):
        cl = self.x264.getColumnList( 2 )
        for i in range( len( cl ) ):
            if not cl[i] == 'Completed':
                self.x264.setListItem( i, 2, message.data )

    def updateColumns( self, column, data ):
        id = self.x264.getColumnItemIndex( 0, self.currentProcessingDirectory )
        self.x264.setListItem( id, column, data )

    def loadOptions( self ):
        self.x264.setProfileDirectory( Configuration.get( 'directories',
                                                         'profile' ) )
        self.x264.setInputDirectory( Configuration.get( 'directories',
                                                         'input' ) )
        self.x264.setOutputDirectory( Configuration.get( 'directories',
                                                         'output' ) )
        self.x264.setVideoOutputFormat( Configuration.get( 'videoSettings',
                                                         'outputFormat' ) )
        self.x264.setAudioOutputFormat( Configuration.get( 'audioSettings',
                                                         'outputFormat' ) )
        self.x264.setMuxOutputFormatList( Configuration.get( 'muxSettings',
                                                         'outputFormatList' ) )
        self.x264.setMuxOutputFormat( Configuration.get( 'muxSettings',
                                                         'outputFormat' ) )
        self.x264.setVideoTwoPass( Configuration.get( 'videoSettings',
                                                         'twoPass' ) )
        self.checkProfileDir()

        self.setX264Events()

    def setX264Events( self ):
        self.x264.Bind( wx.EVT_BUTTON, self.eventInputDirectory,
                        self.x264.inputDirectoryButton )
        self.x264.Bind( wx.EVT_BUTTON, self.eventOutputDirectory,
                        self.x264.outputDirectoryButton )
        self.x264.Bind( wx.EVT_BUTTON, self.eventProfileDirectory,
                        self.x264.profileDirectoryButton )
        self.x264.Bind( wx.EVT_COMBOBOX, self.eventChooseProfile,
                        self.x264.chooseProfileComboBox )
        self.x264.Bind( wx.EVT_TEXT, self.eventVideoOutputFormat,
                        self.x264.videoOutputFormatTextCtrl )
        self.x264.Bind( wx.EVT_TEXT, self.eventVideoCmdOptions,
                        self.x264.videoCmdOptionsTextCtrl )
        self.x264.Bind( wx.EVT_CHECKBOX, self.eventVideoTwoPass,
                        self.x264.videoTwoPassCheckBox )
        self.x264.Bind( wx.EVT_TEXT, self.eventAudioOutputFormat,
                        self.x264.audioOutputFormatTextCtrl )
        self.x264.Bind( wx.EVT_TEXT, self.eventAudioCmdOptions,
                        self.x264.audioCmdOptionsTextCtrl )
        self.x264.Bind( wx.EVT_TEXT, self.eventAudioBitrate,
                        self.x264.audioBitrateTextCtrl )
        self.x264.Bind( wx.EVT_TEXT, self.eventAudioFrequencySample,
                        self.x264.audioFrequencySampleCheckBox )
        self.x264.Bind( wx.EVT_COMBOBOX, self.eventMuxOutputFormat,
                        self.x264.muxOutputFormatComboBox )
        self.x264.Bind( wx.EVT_BUTTON, self.eventAddTask,
                        self.x264.addTaskButton )
        self.x264.Bind( wx.EVT_BUTTON, self.eventRemoveTask,
                        self.x264.removeTaskButton )
        self.x264.Bind( wx.EVT_BUTTON, self.eventPreviewTask,
                        self.x264.previewTaskButton )
        self.x264.Bind( wx.EVT_BUTTON, self.eventRunAll,
                        self.x264.runAllButton )

    def eventAddTask( self, event ):
        if self.checkIntegrity():
            if self.x264.getInputDirectory() in self.x264.getColumnList( 0 ):
                wx.MessageBox( 'Directory already in the list!', 'Warning',
                               wx.OK )
            else:
                columns = []
                columns.append( self.x264.getInputDirectory() )
                columns.append( "" )
                columns.append( "Added" )
                id = self.x264.addListItem( columns )
                self.x264Model.addTask( id, self.x264.getTaskOptions() )
                publisher.sendMessage( 'LOG', 'i6' )

    def eventRemoveTask( self, event ):
        item = self.x264.getQueueList().GetFocusedItem()
        if item > -1:
            self.x264.getQueueList().DeleteItem( item )
            self.x264Model.removeTask( item )
            publisher.sendMessage( 'LOG', 'i7' )

    def eventPreviewTask( self, event ):
        item = self.x264.getQueueList().GetFocusedItem()
        if item > -1:
            task = self.x264Model.getTask( item )
            PreviewController( task )

    def eventRunAll( self, event ):
        self.x264.disableButtons()
        taskQueue = self.x264Model.getTaskQueue()
        rc = RunController( taskQueue )
        publisher.sendMessage( 'LOG', 'i8' )

    def eventInputDirectory( self, event ):
        dlg = wx.DirDialog( self.x264, "Choose an input directory",
                            defaultPath = Configuration.get( 'directories',
                                                         'input' ) )
        if dlg.ShowModal() == wx.ID_OK:
            input = dlg.GetPath()
            if QC.regex( input, '^[A-Z]:$' ):
                input += '\\'
            Configuration.set( input, 'directories', 'input' )
            self.x264.setInputDirectory( input )
        dlg.Destroy()

    def eventOutputDirectory( self, event ):
        dlg = wx.DirDialog( self.x264, "Choose an output directory",
                            defaultPath = Configuration.get( 'directories',
                                                         'output' ) )
        if dlg.ShowModal() == wx.ID_OK:
            output = dlg.GetPath()
            if QC.regex( output, '^[A-Z]:$' ):
                self.output += '\\'
            Configuration.set( output, 'directories', 'output' )
            self.x264.setOutputDirectory( output )
        dlg.Destroy()

    def eventProfileDirectory( self, event ):
        dlg = wx.DirDialog( self.x264, "Choose the profile directory",
                            defaultPath = Configuration.get( 'directories',
                                                         'profile' ) )
        if dlg.ShowModal() == wx.ID_OK:
            profile = dlg.GetPath()
            if QC.regex( profile, '^[A-Z]:$' ):
                self.profile += '\\'
            Configuration.set( profile, 'directories', 'profile' )
            self.x264.setProfileDirectory( profile )
            self.checkProfileDir()
        dlg.Destroy()

    def eventChooseProfile( self, event ):
        profile = os.path.join( self.x264.getProfileDirectory(),
                                          self.x264.getProfile() )
        Configuration.set( profile, 'profile' )
        with open( profile, 'r' ) as f:
            data = f.read()
        lines = data.split( '\n' )
        Configuration.set( lines[0], 'videoSettings', 'cmdOptions' )
        Configuration.set( lines[1], 'audioSettings', 'bitrate' )
        self.x264.setVideoCmdOptions( lines[0] )
        self.x264.setAudioBitrate( lines[1] )

    def eventVideoOutputFormat( self, event ):
        Configuration.set( self.x264.getVideoOutputFormat(), 'videoSettings',
                           'outputFormat' )

    def eventVideoCmdOptions( self, event ):
        Configuration.set( self.x264.getVideoCmdOptions() , 'videoSettings',
                           'cmdOptions' )

    def eventVideoTwoPass( self, event ):
        Configuration.set( self.x264.getVideoTwoPass(), 'videoSettings',
                           'twoPass' )

    def eventAudioOutputFormat( self, event ):
        Configuration.set( self.x264.getAudioOutputFormat(), 'audioSettings',
                           'outputFormat' )

    def eventAudioCmdOptions( self, event ):
        Configuration.set( self.x264.getAudioCmdOptions(), 'audioSettings',
                           'cmdOptions' )

    def eventAudioBitrate( self, event ):
        Configuration.set( self.x264.getAudioBitrate(), 'audioSettings',
                           'bitrate' )

    def eventMuxOutputFormat( self, event ):
        Configuration.set( self.x264.getMuxOutputFormat(), 'muxSettings',
                           'outputFormat' )

    def eventAudioFrequencySample( self, event ):
        Configuration.set( self.x264.getAudioFrequencySample(), 'audioSettings',
                           'frequencySample' )

    def checkProfileDir( self ):
        profiles = QC.loadFiles( self.x264.getProfileDirectory(), 'prfl' )
        self.x264.setProfilesList( sorted( profiles ) )

    def checkIntegrity( self ):
        if not self.x264.getInputDirectory():
            wx.MessageBox( 'No input directory is chosen!', 'Warning', wx.OK )
            return False
        avsFiles = QC.loadFiles( self.x264.getInputDirectory(), 'avs' )
        if not self.x264.getOutputDirectory():
            wx.MessageBox( 'No output directory is chosen!', 'Warning', wx.OK )
        elif not avsFiles:
            wx.MessageBox( 'There are no AVS files in input directory!', 'Warning', wx.OK )
        elif not self.x264.getProfile():
            wx.MessageBox( 'No profile is chosen!', 'Warning', wx.OK )
        elif not self.x264.getVideoOutputFormat():
            wx.MessageBox( 'No video output format is specified!', 'Warning', wx.OK )
        elif not self.x264.getAudioOutputFormat():
            wx.MessageBox( 'No audio output format is specified!', 'Warning', wx.OK )
#        elif not self.x264.getAudioFrequencySample():
#            wx.MessageBox( 'No frequency sample is specified!', 'Warning', wx.OK )
        elif not self.x264.getMuxOutputFormat():
            wx.MessageBox( 'No mux output format is specified!', 'Warning', wx.OK )
        else:
            return True
        return False
