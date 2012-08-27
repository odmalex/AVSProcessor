def commandLogging( self, phase, type, *args ):
    prefix = upper( type ) + '_'
    if phase == 'init':
        publisher.sendMessage( prefix + "GAUGE", 0 )
        if type == 'mux':
            publisher.sendMessage( prefix + "LABEL", 'Waiting for multiplexing...' )
        else:
            publisher.sendMessage( prefix + "LABEL", 'Extracting ' + type + '...' )
    elif phase == 'start':
            if len( args ) > 0:
                extra = args[0]
            else:
                extra = ''
            publisher.sendMessage( prefix + "GAUGE" )
            if type == 'mux':
                publisher.sendMessage( prefix + "LABEL", 'Multiplexing... 0%' +
                                   extra )
            else:
                publisher.sendMessage( prefix + "LABEL", 'Extracting ' + type +
                                       '... 0%' + extra )

