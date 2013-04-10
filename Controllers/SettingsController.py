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
        pub.subscribe( self.exiting, 'EXITING' )

    def exiting( self, message ):
        try:
            self.settingsView.Destroy()
        except:
            pass

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

            self.HOST_DIR = Configuration.get( 'directories', 'host' )
            if not QC.checkDirectory( self.HOST_DIR ):
                self.HOST_DIR = "."
                pub.sendMessage( 'LOG', arg1='e1' )

            # checking applications and libraries
            for app in Configuration.get( 'applications' ):
                appFile = Configuration.get( 'applications', app )
                if not QC.checkFile( appFile, self.HOST_DIR ):
                    pub.sendMessage( 'LOG', arg1='c2' )
                    exit()

            for lib in Configuration.get( 'libraries' ):
                libFile = Configuration.get( 'libraries', lib )
                if not QC.checkFile( libFile, self.HOST_DIR ):
                    pub.sendMessage( 'LOG', arg1='c3' )
                    exit()
        except:
            wx.MessageBox( 'Error in saving configuration!', 'Warning', wx.OK )
#            self.core.logger_core.warning( "Error in saving configuration" )
