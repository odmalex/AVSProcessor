import wx

class RunView( wx.Frame ):
    """ the run window"""
    def __init__( self, *args, **kwds ):
        # begin wxGlade: runWindow.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__( self, *args, **kwds )
        self.processingFileStaticText = wx.StaticText( self, -1,
                                                       "Processing file:                  " )
        self.static_line_1 = wx.StaticLine( self, -1 )
        self.videoExtractStaticText = wx.StaticText( self, -1,
                                                     "Extracting video..." )
        self.videoExtractGauge = wx.Gauge( self, -1, 100,
                                           style = wx.GA_HORIZONTAL |
                                           wx.GA_SMOOTH )
        self.audioExtractStaticText = wx.StaticText( self, -1,
                                                     "Extracting audio..." )
        self.audioExtractGauge = wx.Gauge( self, -1, 100,
                                           style = wx.GA_HORIZONTAL |
                                           wx.GA_SMOOTH )
        self.muxStaticText = wx.StaticText( self, -1, "Multiplexing..." )
        self.muxGauge = wx.Gauge( self, -1, 100, style = wx.GA_HORIZONTAL |
                                                         wx.GA_SMOOTH )
        self.static_line_4 = wx.StaticLine( self, -1 )
        self.detailsNotebook = wx.Notebook( self, -1, style = 0 )
        self.videoDetailsTab = wx.Panel( self.detailsNotebook, -1 )
        self.videoDetailsTextCtrl = wx.TextCtrl( self.videoDetailsTab, -1, "",
                                                 style = wx.TE_MULTILINE |
                                                 wx.TE_RICH2 )
        self.audioDetailsTab = wx.Panel( self.detailsNotebook, -1 )
        self.audioDetailsTextCtrl = wx.TextCtrl( self.audioDetailsTab, -1, "",
                                                 style = wx.TE_MULTILINE |
                                                 wx.TE_RICH2 )
        self.muxDetailsTab = wx.Panel( self.detailsNotebook, -1 )
        self.muxDetailsTextCtrl = wx.TextCtrl( self.muxDetailsTab, -1, "",
                                               style = wx.TE_MULTILINE |
                                               wx.TE_RICH2 )

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties( self ):
        # begin wxGlade: runWindow.__set_properties
        self.SetTitle( "Processing AVS files" )
        self.SetSize( ( 602, 757 ) )
        self.SetBackgroundColour( wx.Colour( 249, 249, 249 ) )
        self.processingFileStaticText.SetForegroundColour( wx.Colour( 0, 127,
                                                                      255 ) )
        self.processingFileStaticText.SetFont( wx.Font( 8, wx.DEFAULT,
                                                        wx.NORMAL, wx.BOLD, 0,
                                                        "" ) )
        self.videoExtractStaticText.SetFont( wx.Font( 7, wx.DEFAULT, wx.NORMAL,
                                                      wx.BOLD, 0, "" ) )
        self.videoExtractGauge.SetMinSize( ( 550, 20 ) )
        self.audioExtractStaticText.SetFont( wx.Font( 7, wx.DEFAULT, wx.NORMAL,
                                                      wx.BOLD, 0, "" ) )
        self.audioExtractGauge.SetMinSize( ( 550, 20 ) )
        self.muxStaticText.SetFont( wx.Font( 7, wx.DEFAULT, wx.NORMAL, wx.BOLD,
                                             0, "" ) )
        self.muxGauge.SetMinSize( ( 550, 20 ) )
        self.videoDetailsTextCtrl.SetMinSize( ( 570, 420 ) )
        self.videoDetailsTextCtrl.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
        self.videoDetailsTextCtrl.SetForegroundColour( wx.Colour( 255, 255,
                                                                  255 ) )
        self.videoDetailsTextCtrl.SetFont( wx.Font( 8, wx.MODERN, wx.NORMAL,
                                                    wx.NORMAL, 0, "" ) )
        self.audioDetailsTextCtrl.SetMinSize( ( 570, 320 ) )
        self.audioDetailsTextCtrl.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
        self.audioDetailsTextCtrl.SetForegroundColour( wx.Colour( 255, 255,
                                                                  255 ) )
        self.audioDetailsTextCtrl.SetFont( wx.Font( 8, wx.MODERN, wx.NORMAL,
                                                    wx.NORMAL, 0, "" ) )
        self.muxDetailsTextCtrl.SetMinSize( ( 570, 320 ) )
        self.muxDetailsTextCtrl.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
        self.muxDetailsTextCtrl.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        self.muxDetailsTextCtrl.SetFont( wx.Font( 8, wx.MODERN, wx.NORMAL,
                                                  wx.NORMAL, 0, "" ) )
        # end wxGlade

    def __do_layout( self ):
        # begin wxGlade: runWindow.__do_layout
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        muxDetailsSizer = wx.BoxSizer( wx.HORIZONTAL )
        audioDetailsSizer = wx.BoxSizer( wx.HORIZONTAL )
        videoDetailsSizer = wx.BoxSizer( wx.HORIZONTAL )
        mainSizer.Add( self.processingFileStaticText, 0, wx.ALL, 5 )
        mainSizer.Add( self.static_line_1, 0, wx.EXPAND, 0 )
        mainSizer.Add( self.videoExtractStaticText, 0, wx.LEFT | wx.TOP |
                       wx.ALIGN_CENTER_VERTICAL, 10 )
        mainSizer.Add( self.videoExtractGauge, 0, wx.ALL | wx.EXPAND, 5 )
        mainSizer.Add( self.audioExtractStaticText, 0, wx.LEFT | wx.TOP, 10 )
        mainSizer.Add( self.audioExtractGauge, 0, wx.ALL | wx.EXPAND, 5 )
        mainSizer.Add( self.muxStaticText, 0, wx.LEFT | wx.TOP, 10 )
        mainSizer.Add( self.muxGauge, 0, wx.ALL | wx.EXPAND, 5 )
        mainSizer.Add( self.static_line_4, 0, wx.EXPAND, 0 )
        videoDetailsSizer.Add( self.videoDetailsTextCtrl, 0, wx.EXPAND, 0 )
        self.videoDetailsTab.SetSizer( videoDetailsSizer )
        audioDetailsSizer.Add( self.audioDetailsTextCtrl, 0, wx.EXPAND, 0 )
        self.audioDetailsTab.SetSizer( audioDetailsSizer )
        muxDetailsSizer.Add( self.muxDetailsTextCtrl, 0, wx.EXPAND, 0 )
        self.muxDetailsTab.SetSizer( muxDetailsSizer )
        self.detailsNotebook.AddPage( self.videoDetailsTab, "Video logs" )
        self.detailsNotebook.AddPage( self.audioDetailsTab, "Audio logs" )
        self.detailsNotebook.AddPage( self.muxDetailsTab, "Mux logs" )
        mainSizer.Add( self.detailsNotebook, 1, wx.ALL | wx.EXPAND, 1 )
        self.SetSizer( mainSizer )
        self.Layout()

    def setProcessingFileText( self, t ):
        self.processingFileStaticText.SetLabel( t )

    def setVideoExtractText( self, t ):
        self.videoExtractStaticText.SetLabel( t )

    def setVideoExtractGauge( self, g ):
        self.videoExtractGauge.SetValue( g )

    def setAudioExtractText( self, t ):
        self.audioExtractStaticText.SetLabel( t )

    def setAudioExtractGauge( self, g ):
        self.audioExtractGauge.SetValue( g )

    def setMuxExtractText( self, t ):
        self.muxExtractStaticText.SetLabel( t )

    def setMuxExtractGauge( self, g ):
        self.muxExtractGauge.SetValue( g )

    def addVideoDetails( self, d ):
        self.videoDetailsTextCtrl.AppendText( d )

    def addAudioDetails( self, d ):
        self.audioDetailsTextCtrl.AppendText( d )

    def addMuxDetails( self, d ):
        self.muxDetailsTextCtrl.AppendText( d )

