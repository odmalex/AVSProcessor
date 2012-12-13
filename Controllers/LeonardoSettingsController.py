import wx
import os
from pubsub import  pub
from Views.LeonardoSettingsView import LeonardoSettingsView
from Models.LeonardoSettingsModel import LeonardoSettingsModel
from Models.Configuration import Configuration
from Models.QC import QC
publisher = pub.Publisher()

class LeonardoSettingsController:
    def __init__( self, panel ):
        self.x264 = panel
        self.leonardoSettingsView = LeonardoSettingsView( None, -1, "" )
        self.leonardoSettingsModel = LeonardoSettingsModel()
        self.setLeonardoSettingsEvents()
        self.leonardo = Configuration.get( 'leonardo' )
        self.updateLists()
        self.leonardoSettingsView.Show()

    def setLeonardoSettingsEvents( self ):
        self.leonardoSettingsView.Bind( wx.EVT_CLOSE, self.eventExit )
        self.leonardoSettingsView.Bind( wx.EVT_BUTTON, self.eventOKButton,
                           self.leonardoSettingsView.okButton )

    def eventOKButton( self, event ):
        language = self.leonardoSettingsView.getLanguage()
        variant = self.leonardoSettingsView.getVariant()
        owner = self.leonardoSettingsView.getOwner()
        aspectRatio = self.leonardoSettingsView.getAspectRatio()
        copyright = self.leonardoSettingsView.getCopyright()

        Configuration.set( self.leonardo['language_list'][language], 'leonardo', 'language' )
        Configuration.set( self.leonardo['variant_list'][variant], 'leonardo', 'variant' )
        Configuration.set( self.leonardo['owner_list'][owner], 'leonardo', 'owner' )
        Configuration.set( self.leonardo['aspect_ratio_list'][aspectRatio], 'leonardo', 'aspect_ratio' )
        Configuration.set( self.leonardo['copyright_list'][copyright], 'leonardo', 'copyright' )

        self.x264.leonardo_settings = False
        self.leonardoSettingsView.Destroy()

    def eventExit( self, event ):
        self.x264.leonardo_settings = False
        self.leonardoSettingsView.Destroy()


    def updateLists( self ):
        lists = self.leonardoSettingsModel.loadLists()

        self.leonardoSettingsView.setLanguageList( lists[0] )
        self.leonardoSettingsView.setVariantList( lists[1] )
        self.leonardoSettingsView.setOwnerList( lists[2] )
        self.leonardoSettingsView.setAspectRatioList( lists[3] )
        self.leonardoSettingsView.setCopyrightList( lists[4] )

        language = QC.getKeyByValue( self.leonardo['language_list'], self.leonardo['language'] )
        self.leonardoSettingsView.setLanguage( language )
        variant = QC.getKeyByValue( self.leonardo['variant_list'], self.leonardo['variant'] )
        self.leonardoSettingsView.setVariant( variant )
        owner = QC.getKeyByValue( self.leonardo['owner_list'], self.leonardo['owner'] )
        self.leonardoSettingsView.setOwner( owner )
        aspect_ratio = QC.getKeyByValue( self.leonardo['aspect_ratio_list'], self.leonardo['aspect_ratio'] )
        self.leonardoSettingsView.setAspectRatio( aspect_ratio )
        copyright = QC.getKeyByValue( self.leonardo['copyright_list'], self.leonardo['copyright'] )
        self.leonardoSettingsView.setCopyright( copyright )
