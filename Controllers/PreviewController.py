import wx
import os
from Models.QC import QC
from Models.Configuration import Configuration
from Models.Commands import Commands
from Models.PreviewModel import PreviewModel
from Views.PreviewView import PreviewView
from pubsub import  pub
publisher = pub.Publisher()

class PreviewController:
    def __init__( self, task ):
        self.task = task
        self.previewView = PreviewView( None, -1, "" )
        self.previewView.Show()
        self.previewModel = PreviewModel( self.task )
        self.showCommands()

        publisher.subscribe( self.exiting, 'EXITING' )

    def exiting( self, message ):
        self.previewView.Destroy()

    def showCommands( self ):
        avsFiles = self.task.getOptions()['avsFiles']
        commandString = self.previewModel.getPreviewOutput()
        self.previewView.setPreviewText( commandString )
        self.previewView.setPreviewStyle( 0, len( commandString ),
                                      wx.TextAttr( "white" ) )
        for avs in avsFiles:
            start = commandString.index( avs )
            end = start + len( avs )
            self.previewView.setPreviewStyle( start, end, wx.TextAttr( "green" ) )

        for app in Configuration.get( 'applications' ):
            host_dir = Configuration.get( 'directories', 'host' )
            application = Configuration.get( 'applications', app )
            exe = os.path.join( host_dir, os.path.basename( application ) )
            l = QC.allIndeces( commandString, exe )
            for i in l:
                self.previewView.setPreviewStyle( i - 1, i + len( exe ) + 1,
                                              wx.TextAttr( "red" ) )


