import atexit
import sys
from pyVim.connect import SmartConnect, Disconnect
import esxsnapshot.log

__author__ = 'weldpua2008@gmail.com'


def to_esx(server, username, password, port=443):
    try:
        esxsnapshot.log.debug('Trying to connect with provided credentials')
        con = SmartConnect(
            host=server,
            user=username,
            pwd=password,
            port=int(port))
        atexit.register(Disconnect, con)
        esxsnapshot.log.info('Connected to server %s' % server)
        esxsnapshot.log.debug('Server type: %s' % con.get_server_type())
        esxsnapshot.log.debug('API version: %s' % con.get_api_version())
        if not con:
            raise SystemExit("Unable to connect to host with supplied info.")
        return con

    except Exception as error:
        esxsnapshot.log.error(error)
        esxsnapshot.log.debug('Connect error. Program will exit now.')
        sys.exit(1)
