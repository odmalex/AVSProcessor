
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
publisher = pub.Publisher()

class Bootstrap:
    def __init__( self ):
        publisher.sendMessage( 'LOG', 'i1' )
        publisher.subscribe( self.boot, 'HOST_PROMPT_OK' )

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
            Configuration.load( Configuration.configurationFile )
        except:
            publisher.sendMessage( 'LOG', 'c1' )
            exit()

    def preLoad( self ):

        self.setLogListener()
        # checking directories
        self.HOST_DIR = Configuration.get( 'directories', 'host' )
        if not QC.checkDirectory( self.HOST_DIR ):
            self.HOST_DIR = "."
            publisher.sendMessage( 'LOG', 'e1' )

        # checking applications and libraries
        for app in Configuration.get( 'applications' ):
            appFile = Configuration.get( 'applications', app )
            if not QC.checkFile( appFile, self.HOST_DIR ):
                publisher.sendMessage( 'LOG', 'c2' )
                exit()

        for lib in Configuration.get( 'libraries' ):
            libFile = Configuration.get( 'libraries', lib )
            if not QC.checkFile( libFile, self.HOST_DIR ):
                publisher.sendMessage( 'LOG', 'c3' )
                exit()

    def setLogListener( self ):
        self.LOG_DIR = Configuration.get( 'directories', 'log' )
        if not QC.checkDirectory( self.LOG_DIR ):
            self.LOG_DIR = "."
            publisher.sendMessage( 'LOG', 'e2' )
        self.logListener = LogListener( self.LOG_DIR )

if __name__ == '__main__':

    boot = Bootstrap()
