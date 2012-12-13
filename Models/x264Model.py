from Models.Task import Task
from Models.DB import DB

class x264Model:

    def __init__( self ):
        self.__taskQueue = []
        self.db = DB()

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
            print task.getOptions()['id'], task.getOptions()['inputDirectory']

    def updateIDs( self ):
        for i in range( len( self.__taskQueue ) ):
            self.__taskQueue[i].getOptions()['id'] = i

    def getTaskQueue( self ):
        return self.__taskQueue

    def getNewTitleId( self ):
        curr_id = self.db.getMaxTableId( 'title' )
        if curr_id:
            return self.db.getMaxTableId( 'title' ) + 1
        else:
            return 1

    def insertTitle( self, args ):
        self.db.insertTable( 'title', args )

    def insertTitleAssets( self, args ):
        self.db.insertTable( 'title_assets', args )

    def updateTitle( self, id, field, value ):
        self.db.updateTable( 'title', id, field, value )
