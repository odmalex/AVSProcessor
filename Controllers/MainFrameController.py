import wx
import os
from pubsub import  pub
from pprint import pprint
from Models.Configuration import Configuration
from Models.QC import QC
from Views.MainFrameView import MainFrameView
from Views.x264View import x264View
from Views.RunView import RunView
from Views.PreviewView import PreviewView
from Views.SettingsView import SettingsView
from x264Controller import x264Controller
from PreviewController import PreviewController
from RunController import RunController
from SettingsController import SettingsController
publisher = pub.Publisher()

class MainFrameController:
    def __init__( self ):
        wx.InitAllImageHandlers()
        self.boot( '' )

    def boot( self, message ):
        self.mainFrame = MainFrameView( None, -1, "" )
        self.mainFrame.x264 = x264View( self.mainFrame )
        self.x264 = self.mainFrame.x264
        self.x264Controller = x264Controller( self.x264 )

        self.setMainFrameEvents()
        self.mainFrame.Show()


    def setMainFrameEvents( self ):
        self.mainFrame.Bind( wx.EVT_CLOSE, self.eventExit )
        self.mainFrame.Bind( wx.EVT_MENU, self.eventExit,
                              self.mainFrame.menuExit )
        self.mainFrame.Bind( wx.EVT_MENU, self.eventAbout,
                              self.mainFrame.menuAbout )
        self.mainFrame.Bind( wx.EVT_TOOL, self.eventSettings, id = 1 )
        self.mainFrame.Bind( wx.EVT_TOOL, self.eventExit, id = 2 )

    def eventExit( self, event ):
        dlg = wx.MessageDialog( self.mainFrame,
                                "Are you sure you want to exit?",
                                "Exiting AVS Processor", wx.OK | wx.CANCEL )
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.mainFrame.Destroy()
            Configuration.save( Configuration.configurationFile )
            pub.sendMessage( 'LOG', arg1='i10' )
            pub.sendMessage( 'EXITING', message='' )

    def eventSettings( self, event ):
        self.settings = SettingsController()

    def eventAbout( self, event ):
        info = wx.AboutDialogInfo()
        info.SetIcon( wx.Icon( '.\\images\\odmedia.png', wx.BITMAP_TYPE_PNG ) )
        info.SetName( 'AVS Processor' )
        info.SetVersion( '1.3.0' )
        info.SetDescription( 'Compilation of AVS processing tools.' )
        info.SetCopyright( '(C) 2013 - ODMedia' )
        info.SetWebSite( 'http://www.odmedia.nl' )
        #info.SetLicence( licence )
        info.AddDeveloper( 'Alexandros Ntavelos' )
        wx.AboutBox( info )


