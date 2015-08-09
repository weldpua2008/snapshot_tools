import sys
import lib.log
from pysphere import VIException
from pysphere import VIServer

__author__ = 'weldpua2008@gmail.com'


def to_esx(server, username, password):
    con = VIServer()
    try:
        lib.log.debug('Trying to connect with provided credentials')
        con.connect(server, username, password)
        lib.log.info('Connected to server %s' % server)
        lib.log.debug('Server type: %s' % con.get_server_type())
        lib.log.debug('API version: %s' % con.get_api_version())
    except VIException as ins:
        lib.log.error(ins)
        lib.log.debug('Loggin error. Program will exit now.')
        sys.exit()

    return con
