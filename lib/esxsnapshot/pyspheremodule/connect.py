import sys
import esxsnapshot.log
from pysphere import VIException
from pysphere import VIServer

__author__ = 'weldpua2008@gmail.com'


def to_esx(server, username, password):
    con = VIServer()
    try:
        esxsnapshot.log.debug('Trying to connect with provided credentials')
        con.connect(server, username, password)
        esxsnapshot.log.info('Connected to server %s' % server)
        esxsnapshot.log.debug('Server type: %s' % con.get_server_type())
        esxsnapshot.log.debug('API version: %s' % con.get_api_version())
    except VIException as ins:
        esxsnapshot.log.error(ins)
        esxsnapshot.log.debug('Loggin error. Program will exit now.')
        sys.exit()

    return con
