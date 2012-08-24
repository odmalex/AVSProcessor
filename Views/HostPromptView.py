import wx

# begin wxGlade: extracode
# end wxGlade


class HostPromptView( wx.Frame ):
    def __init__( self, *args, **kwds ):
        # begin wxGlade: hostDir.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__( self, *args, **kwds )
        self.hostDirStaticText = wx.StaticText( self, -1, "Choose host directory for applications and libraries" )
        self.hostDirTextCtrl = wx.TextCtrl( self, -1, "" )
        self.hostDirButton = wx.Button( self, -1, "Change..." )
        self.askForHostCheckBox = wx.CheckBox( self, -1, "Don't ask me again" )
        self.okButton = wx.Button( self, -1, "OK" )

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties( self ):
        # begin wxGlade: hostDir.__set_properties
        self.SetTitle( "Application and Libraries directory" )
        self.SetSize( ( 500, 180 ) )
        self.SetBackgroundColour( wx.Colour( 249, 249, 249 ) )
        self.hostDirTextCtrl.SetMinSize( ( 390, -1 ) )
        # end wxGlade

    def __do_layout( self ):
        # begin wxGlade: hostDir.__do_layout
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        askAgainSizer = wx.BoxSizer( wx.HORIZONTAL )
        hostDirSizer = wx.BoxSizer( wx.HORIZONTAL )
        mainSizer.Add( self.hostDirStaticText, 0, wx.ALL, 10 )
        hostDirSizer.Add( self.hostDirTextCtrl, 0, wx.LEFT, 5 )
        hostDirSizer.Add( self.hostDirButton, 0, wx.BOTTOM, 1 )
        mainSizer.Add( hostDirSizer, 1, 0, 0 )
        askAgainSizer.Add( self.askForHostCheckBox, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5 )
        askAgainSizer.Add( self.okButton, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 282 )
        mainSizer.Add( askAgainSizer, 1, 0, 0 )
        self.SetSizer( mainSizer )
        self.Layout()

    def setHostDirectory( self, d ):
        self.hostDirTextCtrl.SetValue( d )

    def getHostDirectory( self ):
        return self.hostDirTextCtrl.GetValue()

    def getAskForHostCheckBox( self ):
        return self.askForHostCheckBox.GetValue()
