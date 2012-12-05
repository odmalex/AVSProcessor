import wx

# begin wxGlade: extracode
# end wxGlade

class LeonardoSettingsView( wx.Frame ):
    def __init__( self, *args, **kwds ):
        # begin wxGlade: LeonardoNaming.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__( self, *args, **kwds )
        self.languageStaticText = wx.StaticText( self, -1, "Language" )
        self.languageComboBox = wx.ComboBox( self, -1, choices = [], style = wx.CB_DROPDOWN )
        self.variantStaticText = wx.StaticText( self, -1, "Variant" )
        self.variantComboBox = wx.ComboBox( self, -1, choices = [], style = wx.CB_DROPDOWN )
        self.ownerStaticText = wx.StaticText( self, -1, "Owner" )
        self.ownerComboBox = wx.ComboBox( self, -1, choices = [], style = wx.CB_DROPDOWN )
        self.aspectRatioStaticText = wx.StaticText( self, -1, "Aspect Ratio" )
        self.aspectRatioComboBox = wx.ComboBox( self, -1, choices = [], style = wx.CB_DROPDOWN )
        self.copyrightStaticText = wx.StaticText( self, -1, "Copyright" )
        self.copyrightComboBox = wx.ComboBox( self, -1, choices = [], style = wx.CB_DROPDOWN )
        self.settingsSizer_staticbox = wx.StaticBox( self, -1, "Settings" )
        self.settingsSizer_staticbox.SetForegroundColour( wx.Colour( 0, 95, 191 ) )
        self.okButton = wx.Button( self, -1, "OK" )

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties( self ):
        # begin wxGlade: LeonardoNaming.__set_properties
        self.SetTitle( "Leonardo Naming Settings" )
        self.SetSize( ( 320, 280 ) )
        self.SetBackgroundColour( wx.Colour( 249, 249, 249 ) )
        self.languageStaticText.SetMinSize( ( 75, 13 ) )
        self.variantStaticText.SetMinSize( ( 75, -1 ) )
        self.ownerStaticText.SetMinSize( ( 75, 13 ) )
        self.aspectRatioStaticText.SetMinSize( ( 75, 13 ) )
        self.copyrightStaticText.SetMinSize( ( 75, 13 ) )
        # end wxGlade

    def __do_layout( self ):
        # begin wxGlade: LeonardoNaming.__do_layout
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        self.settingsSizer_staticbox.Lower()
        settingsSizer = wx.StaticBoxSizer( self.settingsSizer_staticbox, wx.VERTICAL )
        copyrightSizer = wx.BoxSizer( wx.HORIZONTAL )
        aspectRatioSizer = wx.BoxSizer( wx.HORIZONTAL )
        ownerSizer = wx.BoxSizer( wx.HORIZONTAL )
        variantSizer = wx.BoxSizer( wx.HORIZONTAL )
        languageSizer = wx.BoxSizer( wx.HORIZONTAL )
        languageSizer.Add( self.languageStaticText, 0, wx.ALL, 10 )
        languageSizer.Add( self.languageComboBox, 0, wx.ALL, 5 )
        settingsSizer.Add( languageSizer, 1, wx.EXPAND, 0 )
        variantSizer.Add( self.variantStaticText, 0, wx.ALL, 10 )
        variantSizer.Add( self.variantComboBox, 0, wx.ALL, 5 )
        settingsSizer.Add( variantSizer, 1, wx.EXPAND, 0 )
        ownerSizer.Add( self.ownerStaticText, 0, wx.ALL, 10 )
        ownerSizer.Add( self.ownerComboBox, 0, wx.ALL, 5 )
        settingsSizer.Add( ownerSizer, 1, wx.EXPAND, 0 )
        copyrightSizer.Add( self.copyrightStaticText, 0, wx.ALL, 10 )
        copyrightSizer.Add( self.copyrightComboBox, 0, wx.ALL, 5 )
        settingsSizer.Add( copyrightSizer, 1, wx.EXPAND, 0 )
        aspectRatioSizer.Add( self.aspectRatioStaticText, 0, wx.ALL, 10 )
        aspectRatioSizer.Add( self.aspectRatioComboBox, 0, wx.ALL, 5 )
        settingsSizer.Add( aspectRatioSizer, 1, wx.EXPAND, 0 )
        mainSizer.Add( settingsSizer, 1, wx.ALL | wx.EXPAND, 10 )
        mainSizer.Add( self.okButton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10 )
        self.SetSizer( mainSizer )
        self.Layout()
        # end wxGlade

    def updateList( self, comboBox, lista ):
        if lista == []:
            comboBox.Clear()
        else:
            for item in lista:
                comboBox.Append( item )

    def setLanguageList( self, languages ):
        self.updateList( self.languageComboBox, languages )
        self.languageComboBox.SetValue( languages[0] )

    def setVariantList( self, variants ):
        self.updateList( self.variantComboBox, variants )
        self.variantComboBox.SetValue( variants[0] )

    def setOwnerList( self, owners ):
        self.updateList( self.ownerComboBox, owners )
        self.ownerComboBox.SetValue( owners[0] )

    def setAspectRatioList( self, aspectRatios ):
        self.updateList( self.aspectRatioComboBox, aspectRatios )
        self.aspectRatioComboBox.SetValue( aspectRatios[0] )

    def setCopyrightList( self, copyrights ):
        self.updateList( self.copyrightComboBox, copyrights )
        self.copyrightComboBox.SetValue( copyrights[0] )

    def setLanguage( self, language ):
        self.languageComboBox.SetValue( language )

    def setVariant( self, variant ):
        self.variantComboBox.SetValue( variant )

    def setOwner( self, owner ):
        self.ownerComboBox.SetValue( owner )

    def setAspectRatio( self, aspectRatio ):
        self.aspectRatioComboBox.SetValue( aspectRatio )

    def setCopyright( self, copyright ):
        self.copyrightComboBox.SetValue( copyright )

    def getLanguage( self ):
        return self.languageComboBox.GetValue()

    def getVariant( self ):
        return self.variantComboBox.GetValue()

    def getOwner( self ):
        return self.ownerComboBox.GetValue()

    def getAspectRatio( self ):
        return self.aspectRatioComboBox.GetValue()

    def getCopyright( self ):
        return self.copyrightComboBox.GetValue()
