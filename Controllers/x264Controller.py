import wx
import os
import socket
from Views.x264View import x264View
from Models.x264Model import x264Model
from Models.Configuration import Configuration
from Models.QC import QC
from Models.DB import DB
from PreviewController import PreviewController
from RunController import RunController
from LeonardoSettingsController import LeonardoSettingsController
from pubsub import  pub
publisher = pub.Publisher()

class x264Controller:
    def __init__( self, panel ):
        self.x264 = panel
        self.x264Model = x264Model()
        self.loadOptions()

        self.generalId = 0
        self.avsFiles = []

        publisher.subscribe( self.updateQueueProcessingDirectory,
                       'QUEUE_PROCESSING_DIRECTORY' )
        publisher.subscribe( self.updateQueueProcessedFiles,
                             'QUEUE_PROCESSED_FILES' )
        publisher.subscribe( self.updateQueueProcessingStatus,
                       'QUEUE_PROCESSING_STATUS' )
        publisher.subscribe( self.updateQueueProcessingStatuses,
                       'QUEUE_PROCESSING_STATUSES' )
        publisher.subscribe( self.processingFinish, 'PROCESSING_FINISH' )

        self.x264.leonardoSettingsButton.Disable()

    def processingFinish( self, message ):
        self.enableButtons()

    def updateQueueProcessingDirectory( self, message ):
        self.currentProcessingOutputDirectory = message.data

    def updateQueueProcessedFiles( self, message ):
        self.updateColumns( 2, message.data )

    def updateQueueProcessingStatus( self, message ):
        self.updateColumns( 3, message.data )

    def updateQueueProcessingStatuses( self, message ):
        cl = self.getColumnList( 3 )
        for i in range( len( cl ) ):
            if not cl[i] == 'Completed':
                self.setListItem( i, 3, message.data )

    def updateColumns( self, column, data ):
        tasks = self.x264Model.getTaskQueue()
        id = 0
        for task in tasks:
            if task.getOptions()['outputDirectory'] == self.currentProcessingOutputDirectory:
                break
            id += 1
        self.setListItem( id, column, data )

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
        self.x264.Bind( wx.EVT_BUTTON, self.eventLeonardoSettings,
                        self.x264.leonardoSettingsButton )

    def leonardoCase( self ):
        multi_profile_sizes = Configuration.get( 'multi_profile', 'sizes' )
        leonardo = Configuration.all['leonardo']

        filebody = ''
        filebody += leonardo['language'] + '_'
        filebody += leonardo['variant'] + '_'
        filebody += leonardo['owner'] + '_'
        filebody += leonardo['copyright'] + '_'
        filebody += leonardo['aspect_ratio'] + '_'

        for avs in self.avsFiles:
            title_id = self.x264Model.getNewTitleId()
            digits = 6
            prefix = str( title_id ).rjust( digits, '0' )
            inputDir = QC.checkDirectory( os.path.join( self.x264.getInputDirectory(), prefix ) )
            outputDir = QC.checkDirectory( os.path.join( self.x264.getOutputDirectory(), prefix ) )

            avsSource = os.path.join( self.x264.getInputDirectory(), avs )
            avsSourceBody, avsSourceExt = os.path.splitext( avsSource )
            if QC.regex( avs, '_43_' ):
                sizes = multi_profile_sizes['_43_']
            elif QC.regex( avs, '_169_' ):
                sizes = multi_profile_sizes['_169_']
            else:
                print 'Aspect ratio not found in the avs filename. Exiting\n'
                exit()


            ## inserting a row in the title table
            args = ( title_id, prefix, avs, )
            args += ( QC.getKeyByValue( leonardo['language_list'], leonardo['language'] ), )
            args += ( QC.getKeyByValue( leonardo['variant_list'], leonardo['variant'] ), )
            args += ( QC.getKeyByValue( leonardo['owner_list'], leonardo['owner'] ), )
            args += ( QC.getKeyByValue( leonardo['copyright_list'], leonardo['copyright'] ), )
            args += ( QC.getKeyByValue( leonardo['aspect_ratio_list'], leonardo['aspect_ratio'] ), )
            args += ( inputDir, outputDir, )
            args += ( Configuration.all['videoSettings']['twoPass'], )
            args += ( Configuration.all['audioSettings']['frequencySample'], )
            args += ( socket.gethostbyname( socket.gethostname() ), ) ## get the local ip
            args += ( None, None, 'Pending' )

            self.x264Model.insertTitle( args ) ## insert a new title entry reserving its unique id 

            for key in sizes.keys():
                filename = os.path.join( inputDir, prefix + '_' + filebody + key + '.avs' )
                f = open( filename, 'w' )
                f.write( 'AVISource("' + avsSource + '",audio=true)\n' )
                f.write( 'bicubicresize(' + sizes[key][0] + ', ' + sizes[key][1] + ')' )

                outputFile = os.path.basename( filename )[:-3]
                outputFile += Configuration.all['muxSettings']['outputFormat']
                args = ( title_id, outputFile, )
                args += ( int( key ), int( sizes[key][0] ), int( sizes[key][1] ), )

                self.x264Model.insertTitleAssets( args )

            columns = []
            columns.append( inputDir )
            columns.append( self.x264.getProfile() )
            columns.append( "" )
            columns.append( "Added" )
            id = self.addListItem( columns )
            opt = self.getTaskOptions()
            opt['inputDirectory'] = inputDir
            opt['outputDirectory'] = outputDir
            self.x264Model.addTask( id, opt )
            publisher.sendMessage( 'LOG', 'i6' )
            self.generalId += 1


    def eventAddTask( self, event ):
        if self.checkIntegrity():
            output, profile = self.checkOutputDirectory()
            if output:
                wx.MessageBox( 'You have already assigned this output directory to "%s" with \
profile "%s". Please choose a different one.' % ( input, profile ), 'Warning',
                                   wx.OK )
            else:
                if Configuration.all['leonardo']['use']: ################# case of Leonardo naming scheme ################
                    self.leonardoCase()
                else:
                    columns = []
                    columns.append( self.x264.getInputDirectory() )
                    columns.append( self.x264.getProfile() )
                    columns.append( "" )
                    columns.append( "Added" )
                    id = self.addListItem( columns )
                    self.x264Model.addTask( id, self.getTaskOptions() )
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
        self.disableButtons()
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

        if self.x264.getProfile() == 'Leonardo-Multiprofile.Prfl':
            self.x264.leonardoSettingsButton.Enable()
            self.x264.videoCmdOptionsStaticText.Disable()
            self.x264.videoCmdOptionsTextCtrl.Disable()
            self.x264.audioBitrateStaticText.Disable()
            self.x264.audioBitrateTextCtrl.Disable()
            Configuration.set( True, 'leonardo', 'use' )
            Configuration.set( lines[0:4], 'multi_profile', 'arguments' )
            Configuration.set( lines[4], 'multi_profile', 'bitrate' )
        else:
            self.x264.leonardoSettingsButton.Disable()
            Configuration.set( False, 'leonardo', 'use' )
            self.x264.videoCmdOptionsStaticText.Enable()
            self.x264.videoCmdOptionsTextCtrl.Enable()
            self.x264.audioBitrateStaticText.Enable()
            self.x264.audioBitrateTextCtrl.Enable()
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

    def eventLeonardoSettings( self, event ):
        if not self.x264.leonardo_settings:
            LeonardoSettingsController( self.x264 )
            self.x264.leonardo_settings = True

    def eventUseLeonardo( self, event ):
        if self.x264.getUseLeonardo():
            self.x264.leonardoSettingsButton.Enable()
            Configuration.set( True, 'leonardo', 'use' )
        else:
            self.x264.leonardoSettingsButton.Disable()
            Configuration.set( False, 'leonardo', 'use' )

    def checkProfileDir( self ):
        profiles = QC.loadFiles( self.x264.getProfileDirectory(), 'prfl' )
        self.x264.setProfilesList( sorted( profiles ) )

    def checkIntegrity( self ):
        if not self.x264.getInputDirectory():
            wx.MessageBox( 'No input directory is chosen!', 'Warning', wx.OK )
            return False
        self.avsFiles = QC.loadFiles( self.x264.getInputDirectory(), 'avs' )
        if not self.x264.getOutputDirectory():
            wx.MessageBox( 'No output directory is chosen!', 'Warning', wx.OK )
        elif not self.avsFiles:
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

    def getTaskOptions( self ):
        opt = {}
        opt['inputDirectory'] = self.x264.getInputDirectory()
        opt['outputDirectory'] = self.x264.getOutputDirectory()
        opt['profileDirectory'] = self.x264.getProfileDirectory()
        opt['profile'] = self.x264.getProfile()
        opt['videoOutputFormat'] = self.x264.getVideoOutputFormat()
        opt['videoCmdOptions'] = self.x264.getVideoCmdOptions()
        opt['videoTwoPass'] = self.x264.getVideoTwoPass()
        opt['audioOutputFormat'] = self.x264.getAudioOutputFormat()
        opt['audioCmdOptions'] = self.x264.getAudioCmdOptions()
        opt['audioBitrate'] = self.x264.getAudioBitrate()
        opt['audioFrequencySample'] = self.x264.getAudioFrequencySample()
        opt['muxOutputFormat'] = self.x264.getMuxOutputFormat()
        opt['leonardoUse'] = Configuration.get( 'leonardo', 'use' )
        opt['multi_profile'] = Configuration.get( 'multi_profile' )

        return opt

    def addListItem( self, columns ):
        count = self.x264.getQueueList().GetItemCount()
        pos = self.x264.getQueueList().InsertStringItem( count, columns[0] )
        self.x264.getQueueList().SetStringItem( pos, 1, columns[1] )
        self.x264.getQueueList().SetStringItem( pos, 2, columns[2] )
        self.x264.getQueueList().SetStringItem( pos, 3, columns[3] )
        return pos

    def setListItem( self, row, column, data ):
        self.x264.queueListCtrl.SetStringItem( row, column, data )

    def getColumnList( self, column ):
        list = []
        count = self.x264.getQueueList().GetItemCount()
        for row in range( count ):
            item = self.x264.getQueueList().GetItem( itemId = row, col = column )
            list.append( item.GetText() )
        return list

    def checkOutputDirectory( self ):
        tasks = self.x264Model.getTaskQueue()
        for task in tasks:
            output = task.getOptions()['outputDirectory']
            if output == self.x264.getOutputDirectory():
                return ( task.getOptions()['inputDirectory'],
                        task.getOptions()['profile'] )
        return ( 0, 0 )

    def getColumnItemIndex( self, column, data ):
        list = self.getColumnList( column )
        try:
            return list.index( data )
        except:
            return -1

    def enableButtons( self ):
        self.x264.addTaskButton.Enable()
        self.x264.removeTaskButton.Enable()
        self.x264.runAllButton.Enable()

    def disableButtons( self ):
        self.x264.addTaskButton.Disable()
        self.x264.removeTaskButton.Disable()
        self.x264.runAllButton.Disable()
