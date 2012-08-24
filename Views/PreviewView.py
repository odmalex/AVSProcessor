import wx

class PreviewView( wx.Frame ):
    def __init__( self, *args, **kwds ):
        # begin wxGlade: mainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        wx.Frame.__init__( self, *args, **kwds )
        self.previewTextCtrl = wx.TextCtrl( self, -1, "", style = wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_LINEWRAP | wx.TE_WORDWRAP | wx.HSCROLL )

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties( self ):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle( "Preview" )
        self.SetSize( ( 900, 600 ) )
        self.previewTextCtrl.SetMinSize( ( 892, 570 ) )
        self.previewTextCtrl.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
        self.previewTextCtrl.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        self.previewTextCtrl.SetFont( wx.Font( 9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "" ) )
        # end wxGlade

    def __do_layout( self ):
        # begin wxGlade: MyFrame.__do_layout
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        mainSizer.Add( self.previewTextCtrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 1 )
        self.SetSizer( mainSizer )
        self.Layout()
        # end wxGlade

    def setPreviewText( self, t ):
        self.previewTextCtrl.SetValue( t )

    def setPreviewStyle( self, start, end, attr ):
        self.previewTextCtrl.SetStyle( start, end, attr )
