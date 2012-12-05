import os
import re
import shutil

class QC:
    @staticmethod
    def checkDirectory( directory ):
        if not os.path.exists( directory ):
            try:
                os.mkdir( directory )
                return directory
            except:
                return False
        return directory

    @staticmethod
    def checkFile( srcFile, destDir ):
        baseFileName = os.path.basename( srcFile )
        destFile = os.path.join( destDir, baseFileName )

        if not os.path.exists( destFile ):
            try:
                shutil.copyfile( srcFile, destFile )
                return True
            except:
                return False
        return True

    @staticmethod
    def loadFiles( directory, extension ):
        try:
            fileList = []
            for p in os.listdir( directory ):
                f, e = os.path.splitext( p )
                if e[1:].lower() == extension.lower():
                    fileList.append( p )
            return fileList
        except:
            print 'Error'
            return []

    @staticmethod
    def recurseDir( path ):
        all_dirs = []
        all_files = []
        for cdir, subdirs, files in os.walk( path ):
            all_dirs.append( subdirs )
            for file in files:
                all_files.append( os.path.join( cdir, file ) )
        return all_dirs, all_files

    @staticmethod
    def regex( string, pattern ):
        p = re.compile( pattern )
        return p.search( string )

    @staticmethod
    def allIndeces( s, sub ):
        l = []
        i = s.find( sub, 0 )
        while i >= 0:
            l.append( i )
            i = s.find( sub, i + 1 )
        return l
