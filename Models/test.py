def commandLogging( self, phase, type, *args ):
    prefix = upper( type ) + '_'
    if phase == 'init':
        pub.sendMessage( prefix + "GAUGE", arg1=0 )
        if type == 'mux':
            pub.sendMessage( prefix + "LABEL", arg1='Waiting for multiplexing...' )
        else:
            pub.sendMessage( prefix + "LABEL", arg1='Extracting ' + type + '...' )
    elif phase == 'start':
            if len( args ) > 0:
                extra = args[0]
            else:
                extra = ''
            pub.sendMessage( prefix + "GAUGE" )
            if type == 'mux':
                pub.sendMessage( prefix + "LABEL", arg1='Multiplexing... 0%' +
                                   extra )
            else:
                pub.sendMessage( prefix + "LABEL", arg1='Extracting ' + type +
                                       '... 0%' + extra )

