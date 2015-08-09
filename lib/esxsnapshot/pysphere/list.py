import esxsnapshot.log
from datetime import datetime
from pysphere import VIException

__author__ = 'weldpua2008@gmail.com'


def parseSNDate(datetuple):
    t = datetuple
    dt = datetime(*t[:6])
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def snapshot(vm):
    try:
        snapshot_fl = []
        snapshot_list = vm.get_snapshots()
        snapshot_list_len = len(snapshot_list)
        esxsnapshot.log.debug(
            " Found %d snapshot(s). Will take a few secs to list." %
            snapshot_list_len)
        snaptext = ''
        if len(snapshot_list) > 0:
            esxsnapshot.log.info('%d snapshot(s) found.' % snapshot_list_len)
            for snapshot in snapshot_list:
                snapshot_name = snapshot.get_name()
                snapshot_descr = snapshot.get_description()
                snapshot_create_time = parseSNDate(snapshot.get_create_time())
                snapshot_state = snapshot.get_state()
                snapshot_path = snapshot.get_path()
                # snapshot_id = snapshot._mor
                #snaptext = 'Id: %s; Name: %s; Description: %s; Created: %s; State: %s; Path: %s \n' % (snapshot_id, snapshot_name, snapshot.get_description(), parseSNDate(snapshot.get_create_time()), snapshot.get_state(), snapshot.get_path())

                snaptext = 'Name: %s; Description: %s; Created: %s; State: %s; Path: %s \n' % (snapshot_name, snapshot_descr, snapshot_create_time, snapshot_state, snapshot_path)
                esxsnapshot.log.warn(snaptext)
                snapshot_fl.append(snaptext)
            return snapshot_fl
        else:
            esxsnapshot.log.warning('No snapshots found related to this VM')
            return 1
    except VIException as inst:
        esxsnapshot.log.error(inst)
        esxsnapshot.log.error('An unexpected error was encountered.')
        return 0

