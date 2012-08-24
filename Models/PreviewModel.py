from Models.Commands import Commands

class PreviewModel:
    def __init__( self, task ):
        self.task = task

    def getPreviewOutput( self ):
        com = Commands( self.task )
        avsFiles = self.task.getOptions()['avsFiles']

        commandList = []
        for avs in avsFiles:
            commands = com.getCommands( avs )
            commandList.append( avs )
            if self.task.getOptions()['videoTwoPass']:
                commandList.append( commands[0] )
                commandList.append( commands[0] )
                commandList.append( commands[1] )
                commandList.append( commands[2] )
            else:
                commandList += commands
        commandsString = "\n".join( commandList )
        commandsString += '\n'

        return commandsString
