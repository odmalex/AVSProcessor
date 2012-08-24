from Models.Task import Task

class x264Model:

    def __init__( self ):
        self.__taskQueue = []

    def addTask( self, id, options ):
        task = Task()
        task.loadOptions( id, options )
        task.setStatus( 'Added' )
        self.__taskQueue.append( task )

    def removeTask( self, index ):
        del self.__taskQueue[index]
        self.updateIDs()

    def getTask( self, id ):
        return self.__taskQueue[id]


    def getTasks( self ):
        for task in self.__taskQueue:
            print task.options['id'], task.getOptions()['inputDirectory']

    def updateIDs( self ):
        for i in range( len( self.__taskQueue ) ):
            self.__taskQueue[i].getOptions()['id'] = i

    def getTaskQueue( self ):
        return self.__taskQueue
