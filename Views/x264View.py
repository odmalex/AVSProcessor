import wx

class x264View( wx.Panel ):
    def __init__( self, parent ):
        wx.Panel.__init__( self, parent )
        self.parent = parent
        self.x264 = ''

        self.inputDirectoryStaticText = wx.StaticText( self, -1,
                                                       "Input       " )
        self.inputDirectoryTextCtrl = wx.TextCtrl( self, -1, "" )
        self.inputDirectoryButton = wx.Button( self, -1, "Change..." )
        self.outputDirectoryStaticText = wx.StaticText( self, -1, "Output    " )
        self.outputDirectoryTextCtrl = wx.TextCtrl( self, -1, "" )
        self.outputDirectoryButton = wx.Button( self, -1, "Change..." )
        self.directoriesSizer_staticbox = wx.StaticBox( self, -1, "Directories" )
        self.directoriesSizer_staticbox.SetForegroundColour( wx.Colour( 0,
                                                                        95,
                                                                        191 ) )
        self.profileDirectoryStaticText = wx.StaticText( self, -1, "Directory " )
        self.profileDirectoryTextCtrl = wx.TextCtrl( self, -1, "" )
        self.profileDirectoryButton = wx.Button( self, -1, "Change..." )
        self.chooseProfileStaticText = wx.StaticText( self, -1,
                                                      "Choose a profile" )
        self.chooseProfileComboBox = wx.ComboBox( self, -1, choices = [],
                                                  style = wx.CB_DROPDOWN )
        self.profileSizer_staticbox = wx.StaticBox( self, -1, "Profile" )
        self.profileSizer_staticbox.SetForegroundColour( wx.Colour( 0, 95,
                                                                    191 ) )
        self.videoOutputFormatStaticText = wx.StaticText( self, -1,
                                                          "Output format" )
        self.videoOutputFormatTextCtrl = wx.TextCtrl( self, -1, "" )
        self.videoCmdOptionsStaticText = wx.StaticText( self, -1,
                                                        "CMD options   " )
        self.videoCmdOptionsTextCtrl = wx.TextCtrl( self, -1, "" )
        self.videoTwoPassCheckBox = wx.CheckBox( self, -1, "2 pass" )
        self.videoSettingsSizer_staticbox = wx.StaticBox( self, -1,
                                                          "Video Settings" )
        self.videoSettingsSizer_staticbox.SetForegroundColour( wx.Colour( 0,
                                                                          95,
                                                                          191 ) )
        self.audioOutputFormatStaticText = wx.StaticText( self, -1,
                                                          "Output format" )
        self.audioOutputFormatTextCtrl = wx.TextCtrl( self, -1, "" )
        self.audioCmdOptionsStaticText = wx.StaticText( self, -1,
                                                        "CMD options   " )
        self.audioCmdOptionsTextCtrl = wx.TextCtrl( self, -1, "" )
        self.audioBitrateStaticText = wx.StaticText( self, -1,
                                                     "Bitrate            " )
        self.audioBitrateTextCtrl = wx.TextCtrl( self, -1, "" )
        self.audioFrequencySampleCheckBox = wx.CheckBox( self,
                                                         - 1,
                                                         "Frequency sample 44100" )

        self.audioSettingsSizer_staticbox = wx.StaticBox( self, -1,
                                                          "Audio Settings" )
        self.audioSettingsSizer_staticbox.SetForegroundColour( wx.Colour( 0,
                                                                          95,
                                                                          191 ) )
        self.muxOutputFormatStaticText = wx.StaticText( self, -1,
                                                        "Output format " )
        self.muxOutputFormatComboBox = wx.ComboBox( self, -1, choices = [],
                                                    style = wx.CB_DROPDOWN )
        self.muxSettingsSizer_staticbox = wx.StaticBox( self, -1, "MUX Settings" )
        self.muxSettingsSizer_staticbox.SetForegroundColour( wx.Colour( 0,
                                                                        95,
                                                                        191 ) )

        self.queueListCtrl = wx.ListCtrl( self, -1,
                                          size = ( -1, 300 ),
                                          style = wx.LC_REPORT |
                                                            wx.SUNKEN_BORDER )

        self.processingDirectoryColumn = self.queueListCtrl.InsertColumn( 0,
                                                        "Processing directory" )
        self.processedFilesColumn = self.queueListCtrl.InsertColumn( 1,
                                                        "Processed files" )
        self.statusColumn = self.queueListCtrl.InsertColumn( 2, "Status" )
        self.queueListCtrl.SetColumnWidth( self.processingDirectoryColumn, 400 )
        self.queueListCtrl.SetColumnWidth( self.processedFilesColumn, 100 )
        self.addTaskButton = wx.Button( self, -1, "Add task" )
        self.removeTaskButton = wx.Button( self, -1, "Remove task" )
        self.previewTaskButton = wx.Button( self, -1, "Preview task" )
        self.runAllButton = wx.Button( self, -1, "Run all" )
        self.static_line_3 = wx.StaticLine( self, -1 )

        self.__set_properties()
        self.__do_layout()

    def __set_properties( self ):
        # begin wxGlade: mainFrame.__set_properties
        self.inputDirectoryTextCtrl.SetMinSize( ( 500, -1 ) )
        self.inputDirectoryButton.SetMinSize( ( 60, 22 ) )
        self.outputDirectoryTextCtrl.SetMinSize( ( 500, -1 ) )
        self.outputDirectoryButton.SetMinSize( ( 60, 22 ) )
        self.profileDirectoryTextCtrl.SetMinSize( ( 500, -1 ) )
        self.profileDirectoryButton.SetMinSize( ( 60, 22 ) )
        self.chooseProfileComboBox.SetMinSize( ( 230, 21 ) )
        self.videoOutputFormatTextCtrl.SetMinSize( ( 115, -1 ) )
        self.videoCmdOptionsTextCtrl.SetMinSize( ( 115, -1 ) )
        self.audioOutputFormatTextCtrl.SetMinSize( ( 115, -1 ) )
        self.audioCmdOptionsTextCtrl.SetMinSize( ( 115, -1 ) )
        self.audioBitrateTextCtrl.SetMinSize( ( 115, -1 ) )
        self.muxOutputFormatComboBox.SetMinSize( ( 115, 21 ) )

    def __do_layout( self ):
        # begin wxGlade: mainFrame.__do_layout
        mainSizer = wx.FlexGridSizer( wx.VERTICAL )
        x264Sizer = wx.GridSizer( 3, 1, 5, 5 )
        buttonsSizer = wx.BoxSizer( wx.HORIZONTAL )
        settingsSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.muxSettingsSizer_staticbox.Lower()
        muxSettingsSizer = wx.StaticBoxSizer( self.muxSettingsSizer_staticbox,
                                              wx.HORIZONTAL )
        muxSettingsSubSizer = wx.BoxSizer( wx.VERTICAL )
        muxOutputFormatSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.audioSettingsSizer_staticbox.Lower()
        audioSettingsSizer = wx.StaticBoxSizer( self.audioSettingsSizer_staticbox,
                                                wx.HORIZONTAL )
        audioSettingsSubtSizer = wx.BoxSizer( wx.VERTICAL )
        audioBitrateSizer = wx.BoxSizer( wx.HORIZONTAL )
        audioOptionsSizer = wx.BoxSizer( wx.HORIZONTAL )
        audioCmdOptionsSizer = wx.BoxSizer( wx.HORIZONTAL )
        audioFrequencySampleSizer = wx.BoxSizer( wx.HORIZONTAL )
        audioOutputFormatSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.videoSettingsSizer_staticbox.Lower()
        videoSettingsSizer = wx.StaticBoxSizer( self.videoSettingsSizer_staticbox,
                                                 wx.HORIZONTAL )
        videoSettingsSubSizer = wx.BoxSizer( wx.VERTICAL )
        videoTwoPassSizer = wx.BoxSizer( wx.HORIZONTAL )
        videoCmdOptionsSizer = wx.BoxSizer( wx.HORIZONTAL )
        videoOutputFormatSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.profileSizer_staticbox.Lower()
        profileSizer = wx.StaticBoxSizer( self.profileSizer_staticbox,
                                          wx.HORIZONTAL )
        profileSubSizer = wx.BoxSizer( wx.VERTICAL )
        chooseProfileSizer = wx.BoxSizer( wx.HORIZONTAL )
        profileDirectorySizer = wx.BoxSizer( wx.HORIZONTAL )
        self.directoriesSizer_staticbox.Lower()
        directoriesSizer = wx.StaticBoxSizer( self.directoriesSizer_staticbox,
                                              wx.HORIZONTAL )
        directoriesSubSizer = wx.BoxSizer( wx.VERTICAL )
        directoriesOutputSizer = wx.BoxSizer( wx.HORIZONTAL )
        directoriesInputSizer = wx.BoxSizer( wx.HORIZONTAL )
        directoriesInputSizer.Add( self.inputDirectoryStaticText, 0, wx.ALL |
                                   wx.ALIGN_CENTER_VERTICAL, 5 )
        directoriesInputSizer.Add( self.inputDirectoryTextCtrl, 0, wx.TOP |
                                   wx.ALIGN_CENTER_VERTICAL, 1 )
        directoriesInputSizer.Add( self.inputDirectoryButton, 0,
                                   wx.ALIGN_CENTER_VERTICAL, 0 )
        directoriesSubSizer.Add( directoriesInputSizer, 1, 0, 0 )
        directoriesOutputSizer.Add( self.outputDirectoryStaticText, 0, wx.ALL |
                                    wx.ALIGN_CENTER_VERTICAL, 5 )
        directoriesOutputSizer.Add( self.outputDirectoryTextCtrl, 0, wx.LEFT |
                                    wx.TOP | wx.ALIGN_CENTER_VERTICAL, 1 )
        directoriesOutputSizer.Add( self.outputDirectoryButton, 0,
                                    wx.ALIGN_CENTER_VERTICAL, 0 )
        directoriesSubSizer.Add( directoriesOutputSizer, 1, 0, 0 )
        directoriesSizer.Add( directoriesSubSizer, 1, wx.EXPAND, 0 )
        x264Sizer.Add( directoriesSizer, 1, wx.ALL | wx.EXPAND, 10 )
        profileDirectorySizer.Add( self.profileDirectoryStaticText, 0, wx.ALL |
                                   wx.ALIGN_CENTER_VERTICAL, 5 )
        profileDirectorySizer.Add( self.profileDirectoryTextCtrl, 0, wx.TOP |
                                   wx.ALIGN_CENTER_VERTICAL, 1 )
        profileDirectorySizer.Add( self.profileDirectoryButton, 0,
                                   wx.ALIGN_CENTER_VERTICAL, 0 )
        profileSubSizer.Add( profileDirectorySizer, 1, 0, 0 )
        chooseProfileSizer.Add( self.chooseProfileStaticText, 0, wx.ALL |
                                wx.ALIGN_CENTER_VERTICAL, 5 )
        chooseProfileSizer.Add( self.chooseProfileComboBox, 0, wx.ALL |
                                wx.ALIGN_CENTER_VERTICAL, 5 )
        profileSubSizer.Add( chooseProfileSizer, 1, 0, 0 )
        profileSizer.Add( profileSubSizer, 1, wx.EXPAND, 0 )
        x264Sizer.Add( profileSizer, 1, wx.ALL | wx.EXPAND, 10 )
        videoOutputFormatSizer.Add( self.videoOutputFormatStaticText, 0, wx.ALL |
                                    wx.ALIGN_CENTER_VERTICAL, 5 )
        videoOutputFormatSizer.Add( self.videoOutputFormatTextCtrl, 0, wx.TOP |
                                    wx.ALIGN_CENTER_VERTICAL, 1 )
        videoSettingsSubSizer.Add( videoOutputFormatSizer, 1, 0, 0 )
        videoCmdOptionsSizer.Add( self.videoCmdOptionsStaticText, 0, wx.ALL |
                                  wx.ALIGN_CENTER_VERTICAL, 5 )
        videoCmdOptionsSizer.Add( self.videoCmdOptionsTextCtrl, 0,
                                  wx.ALIGN_CENTER_VERTICAL, 1 )
        videoSettingsSubSizer.Add( videoCmdOptionsSizer, 1, 0, 0 )
        videoTwoPassSizer.Add( self.videoTwoPassCheckBox, 0, wx.ALL |
                               wx.ALIGN_CENTER_VERTICAL, 5 )
        videoSettingsSubSizer.Add( videoTwoPassSizer, 1, wx.EXPAND, 0 )
        videoSettingsSizer.Add( videoSettingsSubSizer, 1, wx.EXPAND, 0 )
        settingsSizer.Add( videoSettingsSizer, 1, wx.EXPAND, 0 )

        audioOutputFormatSizer.Add( self.audioOutputFormatStaticText, 0,
                                    wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        audioOutputFormatSizer.Add( self.audioOutputFormatTextCtrl, 0, wx.TOP |
                                    wx.ALIGN_CENTER_VERTICAL, 1 )
        audioSettingsSubtSizer.Add( audioOutputFormatSizer, 1, 0, 0 )

        audioCmdOptionsSizer.Add( self.audioCmdOptionsStaticText, 0, wx.ALL |
                                  wx.ALIGN_CENTER_VERTICAL, 5 )
        audioCmdOptionsSizer.Add( self.audioCmdOptionsTextCtrl, 0, wx.TOP |
                                  wx.ALIGN_CENTER_VERTICAL, 1 )
        audioSettingsSubtSizer.Add( audioCmdOptionsSizer, 1, wx.EXPAND, 0 )

        audioBitrateSizer.Add( self.audioBitrateStaticText, 0, wx.ALL |
                               wx.ALIGN_CENTER_VERTICAL, 5 )
        audioBitrateSizer.Add( self.audioBitrateTextCtrl, 0, wx.TOP |
                               wx.ALIGN_CENTER_VERTICAL, 1 )
        audioSettingsSubtSizer.Add( audioBitrateSizer, 1, wx.EXPAND, 0 )
        audioFrequencySampleSizer.Add( self.audioFrequencySampleCheckBox, 0,
                                       wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        audioSettingsSubtSizer.Add( audioFrequencySampleSizer, 1, wx.EXPAND, 0 )

        audioSettingsSizer.Add( audioSettingsSubtSizer, 1, wx.EXPAND, 0 )
        settingsSizer.Add( audioSettingsSizer, 1, wx.LEFT | wx.RIGHT |
                           wx.EXPAND, 5 )

        muxOutputFormatSizer.Add( self.muxOutputFormatStaticText, 0, wx.ALL |
                                  wx.ALIGN_CENTER_VERTICAL, 5 )
        muxOutputFormatSizer.Add( self.muxOutputFormatComboBox, 0, wx.ALL |
                                  wx.ALIGN_CENTER_VERTICAL, 5 )
        muxSettingsSubSizer.Add( muxOutputFormatSizer, 1, 0, 0 )
        muxSettingsSizer.Add( muxSettingsSubSizer, 1, wx.EXPAND, 0 )
        settingsSizer.Add( muxSettingsSizer, 1, wx.EXPAND, 0 )

        x264Sizer.Add( settingsSizer, 1, wx.ALL | wx.EXPAND, 10 )


        buttonsSizer.Add( self.addTaskButton, 0, 0, 0 )
        buttonsSizer.Add( self.removeTaskButton, 0, 0, 0 )
        buttonsSizer.Add( self.previewTaskButton, 0, 0, 0 )
        buttonsSizer.Add( self.runAllButton, 0, wx.LEFT, 350 )

#        queueListSizer()
        mainSizer.Add( x264Sizer, 1, wx.ALL | wx.EXPAND, 10 )
        mainSizer.Add( self.static_line_3, 0, wx.EXPAND, 0 )
        mainSizer.Add( buttonsSizer, 1, wx.ALL | wx.EXPAND, 10 )
        mainSizer.Add( self.queueListCtrl, 1, wx.ALL | wx.EXPAND, 1 )
        self.SetSizer( mainSizer )
        #self.SetSizer( x264Sizer )
        self.Layout()
        self.Centre()
        # end wxGlade


    def setInputDirectory( self, d ):
        self.inputDirectoryTextCtrl.SetValue( d )

    def setOutputDirectory( self, d ):
        self.outputDirectoryTextCtrl.SetValue( d )

    def setProfileDirectory( self, d ):
        self.profileDirectoryTextCtrl.SetValue( d )

    def setProfilesList( self, pl ):
        if pl == []:
            #self.warning.Show()
            self.chooseProfileComboBox.Clear()
        else:
            #self.warning.Hide()
            for p in pl:
                self.chooseProfileComboBox.Append( p )

    def setVideoOutputFormat( self, f ):
        self.videoOutputFormatTextCtrl.SetValue( f )

    def setVideoCmdOptions( self, o ):
        self.videoCmdOptionsTextCtrl.SetValue( o )

    def setVideoTwoPass( self, s ):
        self.videoTwoPassCheckBox.SetValue( s )

    def setAudioOutputFormat( self, f ):
        self.audioOutputFormatTextCtrl.SetValue( f )

    def setAudioCmdOptions( self, o ):
        self.audioCmdOptionsTextCtrl.SetValue( o )

    def setAudioBitrate( self, b ):
        self.audioBitrateTextCtrl.SetValue( b )

    def setMuxOutputFormatList( self, ml ):
        for m in ml:
            self.muxOutputFormatComboBox.Append( m )

    def setAudioSampleFrequency( self, f ):
        self.audioFrequencySampleTextCtrl.SetValue( f )

    def setMuxOutputFormat( self, f ):
        self.muxOutputFormatComboBox.SetValue( f )

    def getInputDirectory( self ):
        return self.inputDirectoryTextCtrl.GetValue()

    def getOutputDirectory( self ):
        return self.outputDirectoryTextCtrl.GetValue()

    def getProfileDirectory( self ):
        return self.profileDirectoryTextCtrl.GetValue()

    def getProfile( self ):
        return self.chooseProfileComboBox.GetValue()

    def getVideoOutputFormat( self ):
        return self.videoOutputFormatTextCtrl.GetValue()

    def getVideoCmdOptions( self ):
        return self.videoCmdOptionsTextCtrl.GetValue()

    def getVideoTwoPass( self ):
        return self.videoTwoPassCheckBox.GetValue()

    def getAudioOutputFormat( self ):
        return self.audioOutputFormatTextCtrl.GetValue()

    def getAudioCmdOptions( self ):
        return self.audioCmdOptionsTextCtrl.GetValue()

    def getAudioBitrate( self ):
        return self.audioBitrateTextCtrl.GetValue()

    def getMuxOutputFormat( self ):
        return self.muxOutputFormatComboBox.GetValue()

    def getAudioFrequencySample( self ):
        return self.audioFrequencySampleCheckBox.GetValue()

    def getQueueList( self ):
        return self.queueListCtrl

    def getTaskOptions( self ):
        opt = {}
        opt['inputDirectory'] = self.getInputDirectory()
        opt['outputDirectory'] = self.getOutputDirectory()
        opt['profileDirectory'] = self.getProfileDirectory()
        opt['profile'] = self.getProfile()
        opt['videoOutputFormat'] = self.getVideoOutputFormat()
        opt['videoCmdOptions'] = self.getVideoCmdOptions()
        opt['videoTwoPass'] = self.getVideoTwoPass()
        opt['audioOutputFormat'] = self.getAudioOutputFormat()
        opt['audioCmdOptions'] = self.getAudioCmdOptions()
        opt['audioBitrate'] = self.getAudioBitrate()
        opt['audioFrequencySample'] = self.getAudioFrequencySample()
        opt['muxOutputFormat'] = self.getMuxOutputFormat()

        return opt

    def addListItem( self, columns ):
        count = self.getQueueList().GetItemCount()
        pos = self.getQueueList().InsertStringItem( count, columns[0] )
        self.getQueueList().SetStringItem( pos, 1, columns[1] )
        self.getQueueList().SetStringItem( pos, 2, columns[2] )
        return pos

    def setListItem( self, row, column, data ):
        self.queueListCtrl.SetStringItem( row, column, data )

    def getColumnList( self, column ):
        list = []
        count = self.getQueueList().GetItemCount()
        for row in range( count ):
            item = self.getQueueList().GetItem( itemId = row, col = column )
            list.append( item.GetText() )
        return list

    def getColumnItemIndex( self, column, data ):
        list = self.getColumnList( column )
        try:
            return list.index( data )
        except:
            return -1

    def enableButtons( self ):
        self.addTaskButton.Enable()
        self.removeTaskButton.Enable()
        self.runAllButton.Enable()

    def disableButtons( self ):
        self.addTaskButton.Disable()
        self.removeTaskButton.Disable()
        self.runAllButton.Disable()
