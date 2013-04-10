

import wx
import os
import sys
sys.path.append( 'C:\\Python27\\Lib\\site-packages\\wx-2.8-msw-unicode' )
sys.path.append( os.path.join( os.getcwd(), '..' ) )
from Models.Configuration import Configuration
from Models.RunModel import RunModel
from Models.QC import QC
from Models.Logger import Logger
from Models.LogListener import LogListener
from MainFrameController import MainFrameController
from HostPromptController import HostPromptController
from pubsub import pub
import win32wnet
publisher = pub.Publisher()

class Bootstrap:
    def __init__( self ):
        pub.sendMessage( 'LOG', arg1='i1' )
        pub.subscribe( self.boot, 'HOST_PROMPT_OK' )
        
        #self.wnet_connect('192.168.247.13', 'administrator', 'g0@')
        
        self.loadConf()
        app = wx.PySimpleApp( 0 )
        if not Configuration.get( 'askForHost' ):
            HostPromptController()
        else:
            self.boot( '' )

        app.MainLoop()
    def boot( self, message ):
        self.preLoad()

        self.mainFrameController = MainFrameController()

    def loadConf( self ):
        # loading configuration
        try:
            Configuration.all = Configuration.load( 'conf\\avs.ini' )
            Configuration.db_conn = Configuration.load( 'conf\\db.ini' )
        except:
            pub.sendMessage( 'LOG', arg1='c1' )
            exit()

    def preLoad( self ):

        self.setLogListener()
        # checking directories
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

    def setLogListener( self ):
        self.LOG_DIR = Configuration.get( 'directories', 'log' )
        if not QC.checkDirectory( self.LOG_DIR ):
            self.LOG_DIR = "."
            pub.sendMessage( 'LOG', arg1='e2' )
        self.logListener = LogListener( self.LOG_DIR )
    
    def wnet_connect(self, host, username, password):
        unc = ''.join(['\\\\', host])
        try:
            win32wnet.WNetAddConnection2(0, None, unc, None, username, password)
        except Exception, err:
            if isinstance(err, win32wnet.error):
                # Disconnect previous connections if detected, and reconnect.
                if err[0] == 1219:
                    win32wnet.WNetCancelConnection2(unc, 0, 0)
                    return wnet_connect(host, username, password)
            raise err

if __name__ == '__main__':

    boot = Bootstrap()
