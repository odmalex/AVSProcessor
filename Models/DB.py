import MySQLdb
import datetime
import socket
from Configuration import Configuration

class DB:

    def __init__( self ):
        #Configuration.all = Configuration.load( '..\\conf\\avs.ini' )
        Configuration.db_conn = Configuration.load( 'conf\\db.ini' )
        self.connect()

    def __del__( self ):
        try:
            self.connection.close()
        except:
            pass

    def connect( self ):
        try:
            self.connection = MySQLdb.connect ( 
                host = Configuration.db_conn['connection']['host'],
                user = Configuration.db_conn['connection']['user'],
                passwd = Configuration.db_conn['connection']['passwd'],
                db = Configuration.db_conn['connection']['db']
            )
            self.cursor = self.connection.cursor()
        except:
            print 'Error in connecting database. Exiting...'
            exit()

    def getMaxTableId( self, table ):
        try:
            line = self.cursor.execute( "SHOW TABLE STATUS LIKE '" + table + "'" )
            return self.cursor.fetchone()[10] - 1
        except:
            print 'Error in fetching max id of table ' + table + '. Exiting...'
            exit()


    def getTableColumns( self, table, str = False ):
        try:
            self.cursor.execute( 'show columns from ' + table )
            results = self.cursor.fetchall()
        except:
            print 'Error in fetching columns of table ' + table + '. Exiting...'
            exit()

        columns = ()
        if results[0][5] == 'auto_increment':
            auto = 1
        else:
            auto = 0
        for res in results:
            columns += ( res[0], )
        return ( columns, auto, )

    def insertTable( self, table, args ):
        sql = 'insert into ' + table + '('
        columns, auto = self.getTableColumns( table )

        if auto:
            sql += ",".join( columns[1:] )
            length = len( columns[1:] )
            arguments = args[1:]
        else:
            sql += ",".join( columns )
            length = len( columns )
            arguments = args
        sql += ') values ('
        values = ( "%s, " * length )
        sql += values[:-2] + ')'

        try:
            self.cursor.execute( sql, arguments )
            self.connection.commit()
        except:
            print 'Error while inserting in table ' + table + '. Exiting...'
            exit()

    def updateTable( self, table, id, field, value ):
        sql = 'update ' + table + ' set ' + field + ' = %s'
        sql += ' where id = ' + str( id )

        try:
            self.cursor.execute( sql, value )
            self.connection.commit()
        except:
            print 'Error while updating table ' + table + '. Exiting...'
            exit()

if __name__ == '__main__':
    db = DB()

#    args = ( Configuration.all['directories']['input'],
#             Configuration.all['directories']['output'],
#             Configuration.all['profile'], True, 0, socket.gethostbyname( socket.gethostname() ),
#             datetime.datetime.now(), datetime.datetime.now() )
#    db.updateTable( 'task', args )
#    id = db.getMaxTableId( 'title' ) + 1
#    jid = str( id ).rjust( 6, '0' )
#    args = ( id, jid, 1, 'aaa.avs', 'english', 'trailer', 'odmedia', 'yes', '16:9' )
#    db.updateTable( 'title', args )
#
#    for size in [250, 500, 800, 1500]:
#        args = ( 1, 'aaa_' + str( size ) + '.avs', size )
#        db.updateTable( 'title_assets', args )

    #db.updateTable( 'title', 1, 'status', 'Completed' )



