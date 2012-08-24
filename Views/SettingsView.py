import wx

class SettingsView( wx.Frame ):
    def __init__( self, *args, **kwds ):
        # begin wxGlade: mainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__( self, *args, **kwds )
        self.settingsStatusbar = self.CreateStatusBar( 1, 0 )

        # Tool Bar
        self.settingsTollbar = wx.ToolBar( self, -1 )
        self.SetToolBar( self.settingsTollbar )
        self.settingsTollbar.AddLabelTool( 1, "Save", wx.Bitmap( "C:\\EclipseWorkspaces\\csse120\\AVS Processor\\images\\save.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, "Save", "Click to save configuration" )
        # Tool Bar end
        self.hostDirectoryStaticText = wx.StaticText( self, -1, "Host    " )
        self.hostDirectoryTextCtrl = wx.TextCtrl( self, -1, "" )
        self.hostDirectoryButton = wx.Button( self, -1, "Change..." )
        self.directoriesSizer_staticbox = wx.StaticBox( self, -1, "Directories" )

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def setHostDirectory( self, d ):
        self.hostDirectoryTextCtrl.SetValue( d )

    def getHostDirectory( self ):
        return self.hostDirectoryTextCtrl.GetValue()

    def __set_properties( self ):
        # begin wxGlade: settings.__set_properties
        self.SetTitle( "Settings" )
        self.SetSize( ( 500, 600 ) )
        self.SetBackgroundColour( wx.Colour( 250, 250, 250 ) )
        self.settingsStatusbar.SetStatusWidths( [-1] )
        # statusbar fields
        settingsStatusbar_fields = [""]
        for i in range( len( settingsStatusbar_fields ) ):
            self.settingsStatusbar.SetStatusText( settingsStatusbar_fields[i], i )
        self.settingsTollbar.Realize()
        self.hostDirectoryTextCtrl.SetMinSize( ( 330, -1 ) )
        # end wxGlade

    def __do_layout( self ):
        # begin wxGlade: settings.__do_layout
        mainSizer = wx.FlexGridSizer( 2, 3, 0, 0 )
        self.directoriesSizer_staticbox.Lower()
        directoriesSizer = wx.StaticBoxSizer( self.directoriesSizer_staticbox, wx.VERTICAL )
        hostDirectorySizer = wx.BoxSizer( wx.HORIZONTAL )
        hostDirectorySizer.Add( self.hostDirectoryStaticText, 0, wx.ALL, 5 )
        hostDirectorySizer.Add( self.hostDirectoryTextCtrl, 0, wx.TOP, 2 )
        hostDirectorySizer.Add( self.hostDirectoryButton, 0, wx.LEFT | wx.TOP, 1 )
        directoriesSizer.Add( hostDirectorySizer, 1, wx.ALL, 5 )
        mainSizer.Add( directoriesSizer, 1, wx.ALL | wx.EXPAND, 5 )
        self.SetSizer( mainSizer )
        self.Layout()
        # end wxGlade
