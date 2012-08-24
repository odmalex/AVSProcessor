import wx
import os
from Views.SettingsView import SettingsView
from Models.Configuration import Configuration
from Models.QC import QC
from pubsub import  pub
publisher = pub.Publisher()

class SettingsController:
    def __init__( self ):
        self.settingsView = SettingsView( None, -1, "" )
        self.settingsView.Show()

        self.hostDirectory = Configuration.get( 'directories', 'host' )

        self.settingsView.setHostDirectory( self.hostDirectory )
        self.setEvents()
        publisher.subscribe( self.exiting, 'EXITING' )

    def exiting( self, message ):
        self.settingsView.Destroy()

    def setEvents( self ):
        self.settingsView.Bind( wx.EVT_TOOL, self.eventSave, id = 1 )
        self.settingsView.Bind( wx.EVT_BUTTON, self.eventHostDirectory,
                            self.settingsView.hostDirectoryButton )

    def eventHostDirectory( self, event ):
        dlg = wx.DirDialog( self.settingsView, "Choose a host directory",
                            defaultPath = self.hostDirectory )
        if dlg.ShowModal() == wx.ID_OK:
            host = dlg.GetPath()
            if QC.regex( host, '^[A-Z]:$' ):
                host += '\\'
            self.settingsView.setHostDirectory( host )
            Configuration.set( host, 'directories', 'host' )
#            self.core.logger_core.info( "New host directory: %s" % self.core.hostDirectory )
        dlg.Destroy()

    def eventSave( self, event ):
        try:
            Configuration.save( Configuration.configurationFile )
            self.settingsView.settingsStatusbar.SetStatusText( "Configuration was saved" )
        except:
            wx.MessageBox( 'Error in saving configuration!', 'Warning', wx.OK )
#            self.core.logger_core.warning( "Error in saving configuration" )
