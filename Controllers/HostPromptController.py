import wx
import os
from pubsub import  pub
from Views.HostPromptView import HostPromptView
from Models.Configuration import Configuration
from Models.QC import QC
publisher = pub.Publisher()

class HostPromptController:
    def __init__( self ):
        self.hostPromptView = HostPromptView( None, -1, "" )
        self.hostDirectory = Configuration.get( 'directories', 'host' )
        self.hostPromptView.setHostDirectory( self.hostDirectory )
        self.setHostDirEvents()
        self.hostPromptView.Show()

    def setHostDirEvents( self ):
        self.hostPromptView.Bind( wx.EVT_BUTTON, self.eventDirectory,
                           self.hostPromptView.hostDirButton )
        self.hostPromptView.Bind( wx.EVT_CHECKBOX, self.eventCheckBox,
                           self.hostPromptView.askForHostCheckBox )
        self.hostPromptView.Bind( wx.EVT_BUTTON, self.eventOKButton,
                           self.hostPromptView.okButton )

    def eventDirectory( self, event ):
        dlg = wx.DirDialog( self.hostPromptView, "Choose an input directory",
                            defaultPath = self.hostDirectory )
        if dlg.ShowModal() == wx.ID_OK:
            host = dlg.GetPath()
            if QC.regex( host, '^[A-Z]:$' ):
                host += '\\'
            Configuration.set( host, 'directories', 'host' )
            self.hostPromptView.setHostDirectory( host )
        dlg.Destroy()

    def eventCheckBox( self, event ):
        ask = self.hostPromptView.getAskForHostCheckBox()
        Configuration.set( ask, 'askForHost' )

    def eventOKButton( self, event ):
        host = self.hostPromptView.getHostDirectory()
        if host == "":
            wx.MessageBox( 'You have to choose a host directory first',
                           'Warning', wx.OK )
        elif not os.path.exists( host ):
            wx.MessageBox( 'This is not a valid directory', 'Warning', wx.OK )
        else:
            self.hostPromptView.Destroy()
            Configuration.set( host, 'directories', 'host' )
            Configuration.save( Configuration.configurationFile )
            pub.sendMessage( 'HOST_PROMPT_OK' )
            pub.sendMessage( 'LOG', arg1='i5' )


