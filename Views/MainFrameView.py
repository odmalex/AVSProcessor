import wx

class MainFrameView( wx.Frame ):
    def __init__( self, *args, **kwds ):
        # begin wxGlade: mainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        wx.Frame.__init__( self, *args, **kwds )


        loc = wx.IconLocation( r'.\\images\\odmedia.ico', 0 )
        self.SetIcon( wx.IconFromLocation( loc ) )

        # Menu Bar
        self.filemenu = wx.Menu()          # Setting up the menu.
        self.helpmenu = wx.Menu()
        self.menuExit = self.filemenu.Append( wx.ID_EXIT, "E&xit",
                                              "Exit AVS Processor" )
        self.menuSettings = self.helpmenu.Append( 1, "&Settings",
                                               " Settings" )
        self.menuAbout = self.helpmenu.Append( wx.ID_ABOUT, "&About",
                                               " About AVS Processor" )
        self.menuBar = wx.MenuBar()
        self.menuBar.Append( self.filemenu, "&File" )
        self.menuBar.Append( self.helpmenu, "&Help" )
        self.SetMenuBar( self.menuBar )
        # Menu Bar end
        self.statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP )

        # Tool Bar
        self.toolBar = wx.ToolBar( self, -1 )
        self.SetToolBar( self.toolBar )
#        self.toolBar.AddLabelTool( 1, "Preview",
#                                   wx.Bitmap( ".\\images\\preview.png",
#                                              wx.BITMAP_TYPE_PNG ),
#                                  wx.NullBitmap, wx.ITEM_NORMAL,
#                                  "Preview",
#                                  "Click to see the commands to be executed" )
#        self.runToolButton = self.toolBar.AddLabelTool( 2,
#                                                        "Run",
#                                                        wx.Bitmap( 
#                                                          ".\\images\\run.png",
#                                                          wx.BITMAP_TYPE_PNG ),
#                                                       wx.NullBitmap,
#                                                       wx.ITEM_NORMAL,
#                                                       "Run",
#                                                  "Click to run the commands" )
        self.settingsToolButton = self.toolBar.AddLabelTool( 1,
                                                             "Settings",
                                                             wx.Bitmap( 
                                                    ".\\images\\settings.png",
                                                    wx.BITMAP_TYPE_PNG ),
                                                            wx.NullBitmap,
                                                            wx.ITEM_NORMAL,
                                                            "Settings",
                                                    "Click to edit settings" )
        self.exitToolButton = self.toolBar.AddLabelTool( 2,
                                                         "Exit",
                                                         wx.Bitmap( 
                                                        ".\\images\\exit.png",
                                                        wx.BITMAP_TYPE_PNG ),
                                                        wx.NullBitmap,
                                                        wx.ITEM_NORMAL,
                                                        "Exit",
                                                        "Click to exit" )
        # Tool Bar end

        self.__set_properties()

    def __set_properties( self ):
        self.Center()
        self.SetTitle( "AVS Processor 1.2.1" )
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap( wx.Bitmap( ".\\images\\odmedia.ico",
                                         wx.BITMAP_TYPE_ANY ) )
        self.SetIcon( _icon )
        self.SetSize( ( 690, 780 ) )
        self.SetBackgroundColour( wx.Colour( 246, 246, 246 ) )
        self.SetFont( wx.Font( 8, wx.DEFAULT, wx.NORMAL, wx.NORMAL,
                               0, "MS Shell Dlg 2" ) )
        self.statusBar.SetStatusWidths( [-1] )
        # statusbar fields
        statusBar_fields = [""]
        for i in range( len( statusBar_fields ) ):
            self.statusBar.SetStatusText( statusBar_fields[i], i )
        self.toolBar.SetToolBitmapSize( ( 35, 35 ) )
        self.toolBar.SetMargins( ( 2, 2 ) )
        self.toolBar.Realize()

if __name__ == "__main__":
    pass
